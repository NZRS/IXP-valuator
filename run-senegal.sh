#!/bin/bash

# Fetch the measurements
# python2 fetch-measurements.py --input senegal-msm-id.txt \
#     --output senegal-measurements.json

python2 ixp-customer.py --msm-file senegal-measurements.json \
    --network-file GeoLite2-Country.mmdb \
    --detection country \
    --country SN \
    --save-file senegal-aggregated.json 
