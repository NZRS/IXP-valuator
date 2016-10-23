#!/bin/bash

python2 ixp-customer.py --msm-file argentina-results.json \
    --network-file cabase-networks.json\
    --detection customer \
    --save-file cabase-aggregated-results.json
