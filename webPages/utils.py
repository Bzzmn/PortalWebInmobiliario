import boto3
from django.conf import settings
import uuid

def upload_to_s3(file):
    s3 = boto3.client('s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    file_name = f"{uuid.uuid4()}-{file.name}"
    s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_name)
    
    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    return url