import json
import IxpCustomerTagger
from collections import defaultdict, Counter
import random
from ripe.atlas.sagan import TracerouteResult
import argparse


def decouple(d):
    return dict((k, {'x': v, 'y': [1] * len(v)}) for k, v in d.iteritems())


def single_cdf(a):
    cum = Counter()
    total = 0
    for item in a:
        cum[item] += 1.0
        total += 1.0

    cumsum = 0
    rv = defaultdict(list)
    for k in sorted(cum.keys()):
        cumsum += cum[k]
        rv['x'].append(k)
        rv['y'].append(cumsum/total)

    return rv


def multiple_cdf(d):
    # Iterate over the list of keys in order
    return dict((k, single_cdf(v)) for k, v in d.iteritems())


parser = argparse.ArgumentParser("Analyze IXP benefit from customer PoV")
parser.add_argument('--msm-file', required=True,
                    help="File with measurement results in JSON format")
parser.add_argument('--cust-file', required=True,
                    help="List of customer networks")
parser.add_argument('--save-file', required=True,
                    help="File to save the results")
args = parser.parse_args()


with open(args.cust_file) as f:
    cust_networks = json.load(f)

# Read a list of traceroute results
with open(args.msm_file) as f:
    trace_set = json.load(f)

tagger = IxpCustomerTagger.IxpCustomerTagger(cust_networks=cust_networks)

trace_hops = defaultdict(list)
trace_rtt = defaultdict(list)
# Iterate over a list of traceroute results from RIPE
for trace_res in trace_set:
    trace_obj = TracerouteResult(trace_res)
    trace_tag = tagger.tag(trace_obj)
    trace_hop_c = tagger.extract_hop_count(trace_obj)
    trace_hop_rtt = tagger.extract_max_rtt(trace_obj)

    # Accumulate some results for later analysis
    trace_hops[trace_tag].append(trace_hop_c)
    trace_rtt[trace_tag].append(trace_hop_rtt)

with open(args.save_file, 'wb') as f:
    json.dump({'hops': decouple(trace_hops),
               'rtt': decouple(trace_rtt),
               'hops_cdf': multiple_cdf(trace_hops),
               'rtt_cdf': multiple_cdf(trace_rtt)}, f)

