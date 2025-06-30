import boto3
from botocore.client import Config

# Configura tu cliente R2
r2 = boto3.client(
    's3',
    aws_access_key_id='fa84d3f23e3527482bce3c7e56458925',
    aws_secret_access_key='ee70b8015d187715b31fffc31aed48554f4290596af7cb576b012db15a6fa5c6',
    endpoint_url='https://4290f283a95f956d408d2fb126d0f952.r2.cloudflarestorage.com',
    region_name='auto',
    config=Config(signature_version='s3v4')
)

BUCKET_NAME = 'mipeli-videos'

# Eliminar todos los objetos del bucket
def eliminar_todo():
    print("Eliminando objetos del bucket...")

    continuation_token = None

    while True:
        if continuation_token:
            response = r2.list_objects_v2(Bucket=BUCKET_NAME, ContinuationToken=continuation_token)
        else:
            response = r2.list_objects_v2(Bucket=BUCKET_NAME)

        objetos = response.get('Contents', [])
        if not objetos:
            print("✅ No hay más archivos.")
            break

        for obj in objetos:
            print(f"Borrando: {obj['Key']}")
            r2.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])

        if response.get('IsTruncated'):
            continuation_token = response['NextContinuationToken']
        else:
            break

    print("✅ Eliminación completa.")

if __name__ == "__main__":
    eliminar_todo()
