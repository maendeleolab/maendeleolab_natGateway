#!/usr/bin/env python3

from maendeleolab_lib import *

regions_list = ['us-east-1','us-west-2']

for region in regions_list:
    #creates nat gateway
    make_nat_gateway(
        Gateway_name="NetworkDev1_a",
        Subnet_Id=build_subnet.get_SubnetId("NetworkDev1_Pub_1a", region), 
        Allocation_Id=build_elastic_ip.get_AllocationId("NetworkDev1_a", region), 
        Connectivity="public", 
        Tag_key="Type",
        Tag_value="billable",
        Region=region,
     )

    make_nat_gateway(
        Gateway_name="NetworkDev1_b",
        Subnet_Id=build_subnet.get_SubnetId("NetworkDev1_Pub_1b", region), 
        Allocation_Id=build_elastic_ip.get_AllocationId("NetworkDev1_b", region), 
        Connectivity="public", 
        Tag_key="Type",
        Tag_value="billable",
        Region=region,
     )

# ----------------------------------- End ------------------------------------------


