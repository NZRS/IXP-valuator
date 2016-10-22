import json
from ripe.atlas.cousteau import Probe, ProbeRequest
from ripe.atlas.cousteau.exceptions import APIResponseError
import random
import argparse

parser = argparse.ArgumentParser("Prepare a few configuration files for IXP "
                                 "Customer analysis")
parser.add_argument('--probe-file', required=True,
                    help="File with probe IDs for known customers")
parser.add_argument('--country', required=True,
                    help="Country code to analyze")
parser.add_argument('--cust-file', required=True,
                    help="Save results in this file")
parser.add_argument('--src-file', required=True,
                    help="Save probe list to this file")
args = parser.parse_args()

probe_info = []
country = args.country
cust_probes = set()
with open(args.probe_file) as f:
    for l in f.readlines():
        # Get some info for this probes
        try:
            prb_id = l.rstrip("\n")
            probe = Probe(id=prb_id)
            # Get the IPv4 network for this probe
            print probe.address_v4
            probe_info.append({'id': prb_id,
                               'ipv4': "%s/32" % probe.address_v4})
            cust_probes.add(int(probe.id))
        except APIResponseError:
            print "Probe %s produced an error" % l

# Find all the probes in a country, and remove the selected ones
filter = {'country_code': country}

probes = ProbeRequest(**filter)

non_cust_probes = set()
for probe in probes:
    if probe['id'] not in cust_probes:
        non_cust_probes.add(probe['id'])

with open(args.cust_file, 'wb') as f:
    json.dump([e['ipv4'] for e in probe_info], f)

with open(args.src_file, 'wb') as f:
    json.dump({'customer': list(cust_probes),
              'non-customer': random.sample(non_cust_probes,
                                            len(cust_probes))}, f)
