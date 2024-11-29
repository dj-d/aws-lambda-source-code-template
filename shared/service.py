import backoff
from botocore.exceptions import ClientError

from constant.utils import MAX_RETRIES


def no_request_limit_exceeded_code(e: ClientError | Exception) -> bool:
    return e.response.get('Error', {}).get('Code', 'Unknown') != 'RequestLimitExceeded'


@backoff.on_exception(
    backoff.expo,
    ClientError,
    max_tries=MAX_RETRIES,
    giveup=no_request_limit_exceeded_code
)
def aws_function(_aws_function, **kwargs):
    return _aws_function(**kwargs)


def make_response(status: str = '', error: str = '', message: str = '', data: dict = None) -> dict:
    return {
        'status': status,
        'error': error,
        'message': message,
        'data': data
    }
