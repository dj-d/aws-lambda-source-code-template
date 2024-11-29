import boto3

from constant.logger import DEBUG_MODE

from shared.logger import Logger, LogLevel

# Set up logging
logger = Logger()
if DEBUG_MODE:
    logger.set_log_level(log_level=LogLevel.DEBUG)


def lambda_handler(event, context):
    pass
