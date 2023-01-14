#!/usr/bin/env python3

from maendeleolab_lib.py import * 

maendeleolab_infra=[
        'us-east-1',
        'us-west-2'
        ]

for region in maendeleolab_infra:
    erase_nat_gateway(region)

# -------------------- End -----------------------
