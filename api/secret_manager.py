import json
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


def get_secret(sm_client: boto3.client, secret_name: str) -> dict:
    """
    Get secret from AWS Secret Manager

    :param sm_client: boto3.client: Secret Manager client
    :param secret_name: str: Secret name

    :return: dict: Response
    """
    try:
        response = aws_function(
            sm_client.get_secret_value,
            SecretId=secret_name
        )

        # logger.debug(f'get_secret: {response}')
    except ClientError as e:
        logger.error(f'get_secret: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=json.loads(response['SecretString'])
    )
