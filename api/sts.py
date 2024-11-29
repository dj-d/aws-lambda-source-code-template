import boto3
from botocore.exceptions import ClientError

from constant.logger import DEBUG_MODE
from constant.utils import RESPONSE_STATUS
from constant.sts import TARGET_ROLE_NAME

from shared.logger import Logger, LogLevel
from shared.service import (
    aws_function,
    make_response
)

# Set up logging
logger = Logger()
if DEBUG_MODE:
    logger.set_log_level(LogLevel.DEBUG)


def assume_role(sts_client: boto3.client, role_arn: str = None, role_session_name: str = 'configLambdaExecution'):
    try:
        response = aws_function(
            sts_client.assume_role,
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )

        LOGGER.debug(f'assume_role: {response}')

    except ClientError as e:
        LOGGER.error(f'assume_role: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response['Credentials']
    )


def get_target_account_credential(sts_client: boto3.client, event: dict, account_id: str = None):
    if account_id:
        account_id = account_id
    else:
        account_id = event['accountId']

    role_arn = f'arn:aws:iam::{account_id}:role/{TARGET_ROLE_NAME}'

    credential_response = assume_role(
        sts_client=sts_client,
        role_arn=role_arn
    )

    if credential_response['status'] != RESPONSE_STATUS['success']:
        return credential_response

    return credential_response['data']
