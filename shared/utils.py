import boto3


def get_target_account_client(target_account_credential: dict, service: str, region: str = 'eu-west-1') -> boto3.client:
    """
    Get target account client

    :param target_account_credential: dict: Target account credential
    :param service: str: Service

    :return: boto3.client: Client
    """
    return boto3.client(
        service,
        aws_access_key_id=target_account_credential['AccessKeyId'],
        aws_secret_access_key=target_account_credential['SecretAccessKey'],
        aws_session_token=target_account_credential['SessionToken'],
        region_name=region
    )
