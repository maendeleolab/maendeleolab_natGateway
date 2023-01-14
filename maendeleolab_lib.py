#!/usr/bin/python3

import os, sys, pprint
from build_nat_gateway import region_id, make_nat_gateway, get_NatId
from build_nat_gateway import destroy_nat_gateway, erase_nat_gateway
FPATH = os.environ.get('ENV_FPATH') #ENV_FPATH should be set in your environment variable file
sys.path.append(FPATH+'/cloudNetworkSpecialty/subnets')
sys.path.append(FPATH+'/cloudNetworkSpecialty/elastic_ip')
import build_subnet
import build_elastic_ip

# -------------------------- End ---------------------------
