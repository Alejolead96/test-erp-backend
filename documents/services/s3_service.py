import boto3
from django.conf import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)


""" def upload_to_s3(file_obj, bucket_key, content_type):

    s3_client.upload_fileobj(
        Fileobj=file_obj,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=bucket_key,
        ExtraArgs={"ContentType": content_type},
    )
    return f's3://{settings.AWS_STORAGE_BUCKET_NAME}/{bucket_key}' """


def download_from_s3(bucket_key):

    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': bucket_key,
        },
        ExpiresIn=3600,
    )
    return presigned_url

def generate_presigned_upload_url(bucket_key, content_type):
 
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': bucket_key,
            'ContentType': content_type
        },
        ExpiresIn=3600,
    )
        
    return presigned_url
        
