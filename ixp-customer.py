import json
import IxpCustomerTagger
from collections import defaultdict
import random
from ripe.atlas.sagan import TracerouteResult


def decouple(d):
    return dict((k, {'x': v, 'y': [1] * len(v)}) for k, v in d.iteritems())

# Mock-up networks just to test, it must be a configuration file
cust_networks = ['14.1.78.0/24', '203.97.97.0/24']

# Read a list of traceroute results
with open('results.json') as f:
    trace_big_set = json.load(f)
    for cc, cc_trace_set in trace_big_set.iteritems():
        trace_set = cc_trace_set


tagger = IxpCustomerTagger.IxpCustomerTagger(cust_networks=cust_networks)

trace_hops = defaultdict(list)
trace_rtt = defaultdict(list)
# Iterate over a list of traceroute results from RIPE
for trace_res in random.sample(trace_set, 1000):
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

