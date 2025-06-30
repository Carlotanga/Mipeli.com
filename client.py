
import boto3
from botocore.client import Config

def crear_cliente_r2():
    return boto3.client(
        's3',
        aws_access_key_id='fa84d3f23e3527482bce3c7e56458925',
        aws_secret_access_key='ee70b8015d187715b31fffc31aed48554f4290596af7cb576b012db15a6fa5c6',
        endpoint_url='https://4290f283a95f956d408d2fb126d0f952.r2.cloudflarestorage.com',
        region_name='auto',
        config=Config(signature_version='s3v4')
    )
