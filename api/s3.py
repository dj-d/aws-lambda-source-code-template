import io
import boto3
from botocore.exceptions import ClientError

from constant.logger import DEBUG_MODE
from constant.utils import RESPONSE_STATUS

from shared.logger import Logger, LogLevel
from shared.service import (
    aws_function,
    make_response
)

# Set up logging
logger = Logger()
if DEBUG_MODE:
    logger.set_log_level(LogLevel.DEBUG)


def upload_file(s3_client: boto3.client, file_name: str, bucket_name: str, key: str) -> dict:
    """
    Upload file to S3 bucket

    :param s3_client: boto3.client: S3 client
    :param file_name: str: File name
    :param bucket_name: str: Bucket name
    :param key: str: Key

    :return: dict: Response
    """
    try:
        response = aws_function(
            s3_client.upload_file,
            Filename=file_name,
            Bucket=bucket_name,
            Key=key
        )

        logger.debug(f'upload_file: {response}')
    except ClientError as e:
        logger.error(f'upload_file: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
   )


def put_object(s3_client: boto3.client, bucket_name: str, key: str, body: io.StringIO) -> dict:
    try:
        response = aws_function(
            s3_client.put_object,
            Bucket=bucket_name,
            Key=key,
            Body=body
        )

        logger.debug(f'put_object: {response}')
    except ClientError as e:
        logger.debug(f'put_object: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
   )


def list_objects(s3_client: boto3.client, bucket_name: str, prefix: str = None) -> dict:
    try:
        response = aws_function(
            s3_client.list_objects_v2,
            Bucket=bucket_name,
            Prefix=prefix
        )

        logger.debug(f'list_objects: {response}')
    except ClientError as e:
        logger.debug(f'list_objects: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
    )


def delete_objects(s3_client: boto3.client, bucket_name: str, objects: list) -> dict:
    try:
        response = aws_function(
            s3_client.delete_objects,
            Bucket=bucket_name,
            Delete={
                'Objects': objects
            }
        )

        logger.debug(f'delete_objects: {response}')
    except ClientError as e:
        logger.debug(f'delete_objects: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
    )