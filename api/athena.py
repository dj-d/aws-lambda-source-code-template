import boto3
from botocore.exceptions import ClientError
from time import sleep

from constant.logger import (
    DEBUG_MODE,
    VERBOSE_MODE
)
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


def run_athena_query(athena_client: boto3.client, query: str, database: str, output_location: str) -> dict:
    """
    Run an Athena query

    :param athena_client:
    :param query:
    :param database:
    :param output_location:
    :return:
    """
    try:
        response = aws_function(
            athena_client.start_query_execution,
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': output_location
            }
        )

        if VERBOSE_MODE:
            logger.debug(f'run_athena_query ({query}) - response: {response}')

        query_execution_id = response['QueryExecutionId']
    except ClientError as e:
        logger.exception(f'run_athena_query: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data={
            'query-execution-id': query_execution_id
        }
    )


def get_athena_query_status(athena_client: boto3.client, query_execution_id: str) -> dict:
    """
    Get the status of an Athena query

    :param athena_client:
    :param query_execution_id:
    :return:
    """
    status = RESPONSE_STATUS['queued']
    output_location = ''

    try:
        while status not in [RESPONSE_STATUS['success'], RESPONSE_STATUS['failed'], RESPONSE_STATUS['cancelled']]:
            response = aws_function(
                athena_client.get_query_execution,
                QueryExecutionId=query_execution_id
            )

            if VERBOSE_MODE:
                logger.debug(f'get_athena_query_status - response: {response}')
            else:
                logger.debug(f'get_athena_query_status - status: {response["QueryExecution"]["Status"]["State"]}')

            status = response['QueryExecution']['Status']['State']
            output_location = response['QueryExecution']['ResultConfiguration']['OutputLocation'].split('/')

            sleep(5)
    except ClientError as e:
        logger.exception(f'get_athena_query_status: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=status,
        data={
            'bucket': output_location[2],
            'key': output_location[3]
        }
    )


def get_athena_query_results(athena_client: boto3.client, query_execution_id: str) -> dict:
    """
    Get the results of an Athena query

    :param athena_client:
    :param query_execution_id:
    :return:
    """
    try:
        response = aws_function(
            athena_client.get_query_results,
            QueryExecutionId=query_execution_id
        )

        if VERBOSE_MODE:
            logger.debug(f'get_athena_query_results - response: {response}')
        else:
            logger.debug(f'get_athena_query_results - rows: {len(response["ResultSet"]["Rows"])}')

        if 'NextToken' in response:
            logger.warning('get_athena_query_results - Pagination needed')

            return make_response(
                status=RESPONSE_STATUS['error'],
                error='Pagination needed'
            )
    except ClientError as e:
        logger.exception(f'get_athena_query_results: {e}')

        return make_response(
            status=RESPONSE_STATUS['error'],
            error=str(e)
        )

    return make_response(
        status=RESPONSE_STATUS['success'],
        data=response['ResultSet']
    )


def do_athena_query(athena_client: boto3.client, query: str, database: str, output_location: str) -> dict:
    """
    Run an Athena query and get the results

    :param athena_client:
    :param query:
    :param database:
    :param output_location:
    :return:
    """
    run_response = run_athena_query(
        athena_client=athena_client,
        query=query,
        database=database,
        output_location=output_location
    )

    if run_response['status'] != RESPONSE_STATUS['success']:
        return run_response

    query_execution_id = run_response['data']['query-execution-id']
    status_response = get_athena_query_status(
        athena_client=athena_client,
        query_execution_id=query_execution_id
    )

    if status_response['status'] != RESPONSE_STATUS['success']:
        return status_response

    results_response = get_athena_query_results(
        athena_client=athena_client,
        query_execution_id=query_execution_id
    )

    if results_response['status'] != RESPONSE_STATUS['success']:
        return results_response

    rows = []
    for row in results_response['data']['Rows']:
        rows.append(row['Data'][0]['VarCharValue'])

    return make_response(
        status=RESPONSE_STATUS['success'],
        data={
            'rows': rows
        }
    )
