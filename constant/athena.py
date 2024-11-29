import os

DATABASE_NAME = str(os.getenv(
    key='DATABASE_NAME',
    default='auditing'
))

ACCOUNT_ID_VIEW_NAME = str(os.getenv(
    key='ACCOUNT_ID_VIEW_NAME',
    default='v_account_info'
))

REGION_ID_VIEW_NAME = str(os.getenv(
    key='REGION_ID_VIEW_NAME',
    default='config_rule_resource_compliance_v3'
))

OUTPUT_LOCATION = f"s3://{str(os.getenv(key='OUTPUT_LOCATION', default='aws-athena-query-results-307368338789-eu-west-1'))}/"
