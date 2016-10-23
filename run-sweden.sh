#!/bin/bash

python2 ixp-customer.py --msm-file sweden-results.json \
    --network-file peeringdb-dump.json \
    --detection IXP \
    --save-file sweden-aggregated.json
