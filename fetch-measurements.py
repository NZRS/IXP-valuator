from ripe.atlas.cousteau import AtlasResultsRequest
import json


with open('sweden-msm-id.txt') as f:
    results = []
    for l in f.readlines():
        kwargs = {'msm_id': l.rstrip("\n")}
        is_success, msm_res = AtlasResultsRequest(**kwargs).create()

        if is_success:
            results = results + msm_res

with open('sweden-results.json', 'wb') as f:
    json.dump(results, f)
