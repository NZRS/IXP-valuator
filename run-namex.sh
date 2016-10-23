#!/bin/bash

python2 ixp-customer.py --msm-file namex-results.json \
    --network-file customer-networks.json \
    --detection customer \
    --save-file namex-aggregated.json
