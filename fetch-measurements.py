from ripe.atlas.cousteau import AtlasResultsRequest
import json
import argparse
import re

parser = argparse.ArgumentParser("Retrieves traceroute results")
parser.add_argument('--input', required=True,
                    help="File with measurements IDs")
parser.add_argument('--output', required=True,
                    help="File name to save results")
args = parser.parse_args()


if re.search('\.txt$', args.input):
    with open(args.input) as f:
        msm_ids = [l.rstrip() for l in f.readlines()]
elif re.search('\.json', args.input):
    with open(args.input) as f:
        msm_ids = json.load(f)

results = []
for msm_id in msm_ids:
    kwargs = {'msm_id': msm_id}
    is_success, msm_res = AtlasResultsRequest(**kwargs).create()

    if is_success:
        results = results + msm_res

with open(args.output, 'wb') as f:
    json.dump(results, f)
