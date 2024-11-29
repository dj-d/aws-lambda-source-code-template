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


def get_functions(lambda_client: boto3.client) -> dict:
    """
    Get all Lambda functions
    """

    try:
        response = aws_function(
            lambda_client.list_functions
        )

        LOGGER.debug(f'utils - get_functions - response: {response}')

    except ClientError as e:
        LOGGER.error(f'utils - get_functions - error: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
    )


def get_tags(lambda_client: boto3.client, resource_arn: str) -> dict:
    """
    Get tags from a Lambda function
    """
    try:
        response = aws_function(
            lambda_client.list_tags,
            Resource=resource_arn
        )

        LOGGER.debug(f'utils - get_tag_project - response: {response}')

    except ClientError as e:
        LOGGER.error(f'utils - get_tag_project - error: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response['Tags']
    )
