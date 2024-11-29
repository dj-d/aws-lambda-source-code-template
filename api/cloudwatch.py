import boto3
from botocore.exceptions import ClientError
from datetime import datetime

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


def get_metric_data(cloudwatch_client: boto3.client, metric_data: list, start_time: datetime,
                    end_time: datetime) -> dict:
    """
    Get metric data from CloudWatch
    """
    try:
        response = aws_function(
            cloudwatch_client.get_metric_data,
            MetricDataQueries=metric_data,
            StartTime=start_time,
            EndTime=end_time
        )

        logger.debug(f'utils - get_metric_data - response: {response}')
    except ClientError as e:
        logger.error(f'utils - get_metric_data - error: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response
    )