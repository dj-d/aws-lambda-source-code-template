import os

INSPECTOR_KMS_KEY_ARN = str(os.getenv(
    key='INSPECTOR_KMS_KEY_ARN'
    )
)

INSPECTOR_BUCKET_NAME = str(os.getenv(
    key='INSPECTOR_BUCKET_NAME'
    )
)

INSPECTOR_BUCKET_ARN = f'arn:aws:s3:::{INSPECTOR_BUCKET_NAME}'
