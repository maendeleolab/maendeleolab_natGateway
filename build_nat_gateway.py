#!/usr/bin/env python3

Goal = '''
to create nat-gateway in aws
Author: Pat@Maendeleolab
'''

#Module imports
import logging, sys, os, json
from datetime import datetime
from time import sleep

#Path to local home and user folder
FPATH = os.environ.get('ENV_FPATH')

#logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p ',\
                filename=FPATH + '/maendeleolab_natGateway/nat_gateway.log', level=logging.INFO)

#adding flexibility for regions
def region_id(name='us-east-1'):
    return name # e.g: 'us-east-1'

def verify_nat_gateway(nat_name, region='us-east-1'):
    ''' Verifies if NAT Gateway name already exists '''
    try:
        output = os.popen('aws ec2 describe-nat-gateways --filter Name=tag:Name,Values=' + nat_name + ' --region '+ region).read()
        nat_data = json.loads(str(output))
        if len(nat_data['NatGateways']) > 0:
            print(f'{nat_name} already exists in {region}...')
            return 1
    except Exception as err:
        logging.info(f'Logging "verify_nat_gateway" error: {err}')
        print('Logging "verify_nat_gateway" error in nat_gateway.log...')

#create nat-gateway
def make_nat_gateway(**kwargs):
    try:
        if verify_nat_gateway(kwargs['Gateway_name'], kwargs['Region']) == 1:
            pass
        else:
            os.system("aws ec2 create-nat-gateway \
            --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=" + kwargs['Gateway_name'] + "},\
            {Key=" + kwargs['Tag_key'] + ",Value=" + kwargs['Tag_value'] + "}]'\
            --subnet-id " + kwargs['Subnet_Id'] + "\
            --allocation-id " + kwargs['Allocation_Id'] + "\
            --connectivity-type " + kwargs['Connectivity'] + "\
            --region " + kwargs['Region'] 
            )
            logging.info(f'Created NAT Gateway: {kwargs["Gateway_name"]} in {kwargs["Region"]}...')
            print(f'Created NAT Gateway: {kwargs["Gateway_name"]} in {kwargs["Region"]}...')
    except Exception as err:
        logging.info(f'Logging "make_nat_gateway" error: {err}')
        print('Logging "make_nat_gateway" error in nat_gateway.log...')
        print('Elastic IP API must be called first, before the NAT Gateway...')

def get_NatId(Gateway, region='us-east-1'):
    ''' Gets resource id from json output and can be used in deploy scripts '''
    try:
        output = os.popen('aws ec2 describe-nat-gateways --filter Name=tag:Name,Values=' + Gateway + ' --region ' + region).read()
        nat_gateway_data = json.loads(str(output))
        data = nat_gateway_data['NatGateways']
        for info in data:
            return info['NatGatewayId']
    except Exception as err:
        logging.info(f'Logging "get_NatId" error: {err}')
        print('Logging "get_NatId" error in nat_gateway.log...')

def destroy_nat_gateway(Gateway_Id, region='us-east-1'):
    try:
        os.system('aws ec2 delete-nat-gateway --nat-gateway-id ' + Gateway_Id + ' --region ' + region)
        logging.info(f'Deleted NAT Gateway Id: {Gateway_Id} in {region}...')
        print(f'Deleted NAT Gateway Id: {Gateway_Id} in {region}...')
    except Exception as err:
        logging.info(f'Logging "destroy_nat_gateway" error: {err}')
        print('Logging "destroy_nat_gateway" in nat_gateway.log...')

def erase_nat_gateway(region='us-east-1'):
    try:
        ''' Deletes all NAT Gateways that do not have dependencies '''
        output = os.popen('aws ec2 describe-nat-gateways  --region ' + region).read()
        nat_data = json.loads(str(output))
        for data in nat_data['NatGateways']:
            print('Logging erase_nat ' + data['NatGatewayId'])
            destroy_nat_gateway(data['NatGatewayId'], region=region)
            logging.info(f'Logging erase_nat: {data["NatGatewayId"]} in region: {region}...')

        new_data = json.dumps(data, indent=2)
        print(new_data)
    except Exception as err:
        logging.info(f'Logging "erase_nat_gateway" error: {err}')
        print('Logging "erase_nat_gateway" error in nat_gateway.log...')

# ---------------------------------- End ---------------------------------------


