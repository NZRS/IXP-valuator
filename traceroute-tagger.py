import json
import IxpCrossTagger
from collections import defaultdict
import random
from ripe.atlas.sagan import TracerouteResult


def decouple(d):
    return dict((k, {'x': v, 'y': [1] * len(v)}) for k, v in d.iteritems())

ixp_networks = []
# Read a list of networks from PeeringDB
with open('peeringdb-dump.json') as f:
    pdb = json.load(f)
    for e in pdb:
        ixp_networks = ixp_networks + e['ixpfx']


# Read a list of traceroute results
with open('sweden-results.json') as f:
    trace_set = json.load(f)

tagger = IxpCrossTagger.IxpCrossTagger(ixp_networks=ixp_networks)

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

with open('aggregated-metrics.json', 'wb') as f:
    json.dump({'hops': decouple(trace_hops),
               'rtt': decouple(trace_rtt)}, f)

