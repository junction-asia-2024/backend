import boto3
import os
from dotenv import load_dotenv

load_dotenv()

bucket_region = os.getenv('BUCKET_REGION')
bucket_access_key = os.getenv('BUCKET_ACCESS_KEY')
bucket_secret_key = os.getenv('BUCKET_SECRET_KEY')
bucket_name = os.getenv('BUCKET_NAME')
bucket_url_prefix = os.getenv('BUCKET_URL_PREFIX')

# TODO: singleton으로 수정, presigned URL 사용 여부 논의
def s3_connection():
    try:
        bucket = boto3.client(
            service_name = 's3',
            region_name = bucket_region,
            aws_access_key_id = bucket_access_key,
            aws_secret_access_key = bucket_secret_key
        )
    except Exception as error:
        print(error)
        return { 'code': 500, 'message': '오류가 발생했습니다. 다시 시도해주세요.' }
    else:
        return bucket

s3 = s3_connection()