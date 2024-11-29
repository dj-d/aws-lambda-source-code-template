import os

S3_BUCKET = str(os.getenv(
    key='S3_BUCKET',
    default='yunex-metabase'
    )
)

S3_BUCKET_FOLDER = str(os.getenv(
    key='S3_BUCKET_FOLDER',
    default='map-migrated-tagger-lambda-info'
    )
)
