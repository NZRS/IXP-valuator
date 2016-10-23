from ripe.atlas.sagan import TracerouteResult
import json

with open('gambia-content-measurements.json') as f:
    trace_set = json.load(f)

subset = []
for trace in trace_set:
    if trace['prb_id'] == 18514 and trace['dst_name'] == 'thepoint.gm':
        subset.append(trace)

with open('gambia-subset.json', 'wb') as f:
    json.dump(subset, f)
