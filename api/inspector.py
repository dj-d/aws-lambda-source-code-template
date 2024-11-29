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


def create_findings_report(inspector_client: boto3.client, bucket_arn: str, kms_key_arn: str, report_format: str = "CSV", key_prefix: str= "/") -> dict:
    """
    Create a findings report

    :param inspector_client:
    :param bucket_arn:
    :param kms_key_arn:
    :param report_format:
    :return:
    """

    logger.debug(f'create_findings_report: {bucket_arn} {kms_key_arn} {report_format} {key_prefix}')

    try:
        response = aws_function(
            inspector_client.create_findings_report,
            reportFormat=report_format,
            s3Destination={
                'bucketName': bucket_arn,
                'keyPrefix': key_prefix,
                'kmsKeyArn': kms_key_arn
            }
        )

        logger.debug(f'create_findings_report: {response}')
    except ClientError as e:
        logger.debug(f'create_findings_report: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
    )


def get_finding_report_status(inspector_client: boto3.client, report_id: str) -> dict:
    """
    Get the status of a findings report

    :param inspector_client:
    :param report_id:
    :return:
    """

    try:
        response = aws_function(
            inspector_client.get_findings_report_status,
            reportId=report_id
        )

        logger.debug(f'get_finding_report_status: {response}')
    except ClientError as e:
        logger.debug(f'get_finding_report_status: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
    )