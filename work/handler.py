import boto3
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        logger.info(event)
        SGID = os.environ['SGID']

        c_ec2 = boto3.client('ec2')
        myip = '0.0.0.0'

        c_ec2.authorize_security_group_ingress(
                GroupId=SGID,
                IpPermissions=[
                    {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [
                            {
                            'CidrIp': "{0}/0".format(myip),
                            'Description': 'lambda'
                            },
                        ],
                    },
                    {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [
                            {
                            'CidrIp': "{0}/0".format(myip),
                            'Description': 'lambda'
                            },
                        ],
                    },
                ],
        )
        logger.info('Succeed')
    except Exception as e:
        logger.error(e)
        raise e
