import json
import IxpCustomerTagger
import IxpCrossTagger
import CountryTagger
from collections import defaultdict, Counter
from ripe.atlas.sagan import TracerouteResult
import argparse
import pandas as pd
import numpy as np


def decouple(d):
    return dict((k, {'x': v, 'y': [1] * len(v)}) for k, v in d.iteritems())


def single_cdf(a, var_t):
    df = pd.DataFrame(data={'v': a})
    if var_t == 'hops':
        bins=xrange(0, 30, 1)
    if var_t == 'rtt':
        bins=xrange(0, 200, 5)

    df['bin'] = pd.cut(df['v'], bins=bins, include_lowest=True)
    grp = df.groupby('bin').count().reset_index()
    grp['cum'] = grp['v'].cumsum() / grp['v'].sum()

    return {'x': grp['bin'].tolist(),
            'y': grp['cum'].tolist()}


def multiple_cdf(d, var_t):
    # Iterate over the list of keys in order
    return dict((k, single_cdf(v, var_t)) for k, v in d.iteritems())


def cdf_diff(d, var_t, key_order):
    tmp_cdf = dict((k, single_cdf(v, var_t)) for k, v in d.iteritems())
#    print(tmp_cdf[key_order[0]]['y'])
#    print(tmp_cdf[key_order[1]]['y'])
    new_cdf = {'x': tmp_cdf[key_order[0]]['x'],
               'y': (np.array(tmp_cdf[key_order[0]]['y']) -
                    np.array(tmp_cdf[key_order[1]]['y'])).tolist()}
    return new_cdf


parser = argparse.ArgumentParser("Analyze IXP benefit from customer PoV")
parser.add_argument('--msm-file', required=True,
                    help="File with measurement results in JSON format")
parser.add_argument('--network-file', required=True,
                    help="List of networks to detect")
parser.add_argument('--detection', required=True, default='customer',
                    help="What kind of detection to run")
parser.add_argument('--country', required=False,
                    help="Which country to use for detection='country'")
parser.add_argument('--save-file', required=True,
                    help="File to save the results")
args = parser.parse_args()

if args.detection == 'country' and args.country is None:
    raise argparse.ArgumentError("Detection='country' requires --country "
                                 "parameter")


# Read a list of traceroute results
with open(args.msm_file) as f:
    trace_set = json.load(f)

if args.detection == 'customer':
    with open(args.network_file) as f:
        cust_networks = json.load(f)
    tagger = IxpCustomerTagger.IxpCustomerTagger(cust_networks=cust_networks)
elif args.detection == 'IXP':
    ixp_networks = []
    with open(args.network_file) as f:
        pdb = json.load(f)
        for e in pdb:
            ixp_networks = ixp_networks + e['ixpfx']
    tagger = IxpCrossTagger.IxpCrossTagger(ixp_networks=ixp_networks)
elif args.detection == 'country':
    tagger = CountryTagger.CountryTagger(geo_data=args.network_file,
                                         country=args.country)

trace_hops = defaultdict(list)
trace_rtt = defaultdict(list)
trace_mesh = pd.DataFrame({'src': [], 'dst': [], 'tag': [], 'hop': [],
                           'rtt': [], 'af': []})
# Iterate over a list of traceroute results from RIPE
for trace_res in trace_set:
    trace_obj = TracerouteResult(trace_res)
    if trace_obj.af != 4:
        continue
    trace_tag = tagger.tag(trace_obj)
    trace_hop_c = tagger.extract_hop_count(trace_obj)
    trace_hop_rtt = tagger.extract_max_rtt(trace_obj)

    # An RTT of 0 is an error
    if trace_hop_rtt == 0:
        continue

    # Accumulate some results for later analysis
    trace_hops[trace_tag].append(trace_hop_c)
    trace_rtt[trace_tag].append(trace_hop_rtt)

    # Prepare a mesh of probes and destinations, their "tag" and a value
    trace_mesh = pd.concat([trace_mesh,
                            pd.DataFrame({'src': [tagger.name_probe(trace_tag, trace_obj.probe_id)],
                                          'dst': [trace_obj.destination_name],
                                          'tag': [trace_tag],
                                          'hop': [trace_hop_c],
                                          'af': [trace_obj.af],
                                          'rtt': [trace_hop_rtt]})])

# Sort the dataframe to generate something useful
rtt_values = []
src_list = trace_mesh.sort_values(by=['tag', 'src'])['src'].unique().tolist()
dst_list = trace_mesh['dst'].unique().tolist()
for dst in dst_list:
    row = []
    for src in src_list:
        rtt_set = trace_mesh.query("(src=='%s') & (dst=='%s')" % (src, dst))['rtt']
        if len(rtt_set) > 1:
            row = row + [np.mean(rtt_set)]
        elif len(rtt_set) == 0:
            row = row + [None]
        else:
            row = row + [r for r in rtt_set]
    rtt_values.append(row)
mesh = {'x': src_list, 'y': dst_list, 'z': rtt_values}

with open(args.save_file, 'wb') as f:
    json.dump({'hops': decouple(trace_hops),
               'rtt': decouple(trace_rtt),
               'hops_cdf': multiple_cdf(trace_hops, 'hops'),
               'rtt_cdf': multiple_cdf(trace_rtt, 'rtt'),
               'mesh': mesh}, f)

cols = ['src', 'tag', 'dst', 'hop', 'rtt', 'af']
trace_mesh.sort_values(by=['tag', 'src'])[cols].to_csv('trace-info.csv',
                                                       index=False)
