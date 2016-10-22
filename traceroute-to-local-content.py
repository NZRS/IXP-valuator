import json
from ripe.atlas.cousteau import Traceroute, AtlasSource, AtlasCreateRequest
from datetime import datetime
import os
import argparse


parser = argparse.ArgumentParser("Executes traceroutes to local content")
parser.add_argument('--probe-file', required=True,
                    help="File with probe IDs to use")
parser.add_argument('--dest-file', required=True,
                    help="File with list of destinations")
parser.add_argument('--save-file', required=True,
                    help="Save measurements IDs to this file")
args = parser.parse_args()

with open('%s/.auth/ripe-atlas' % os.environ['HOME']) as f:
    ATLAS_API_KEY = f.readline()[:-1]

# Read list of probes
with open(args.probe_file) as f:
    tmp_prb_src = json.load(f)
    src_probes = []
    for cat, cat_probes in tmp_prb_src.iteritems():
        src_probes = src_probes + cat_probes

# print src_probes
# Read list of destinations
with open(args.dest_file) as f:
    dst_list = [l.rstrip() for l in f.readlines()]


msm_list = []
atlas_src = AtlasSource(
    requested=len(src_probes),
    type="probes",
    value=",".join([str(p) for p in src_probes])
)
# Create the measurements and save the IDs to a file
for dst in dst_list:
    traceroute = Traceroute(af=4, target=dst,
                            description="IXP Valuator to %s" % dst,
                            protocol="ICMP",
                            is_public=True)

    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        key=ATLAS_API_KEY,
        measurements=[traceroute],
        sources=[atlas_src],
        is_oneoff=True
    )

    (is_success, response) = atlas_request.create()
    if is_success:
        for m in response['measurements']:
            msm_list.append(m)

with open(args.save_file, 'wb') as f:
    json.dump(msm_list, f)
