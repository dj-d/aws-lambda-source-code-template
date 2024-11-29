import os

DATE_FORMAT = '%Y-%-m-%d'

DAY_RANGE = int(os.getenv(
    key='DAY_RANGE',
    default=1
))

PERIOD = int(os.getenv(
    key='PERIOD',
    default=1
)) * 24 * 60 * 60
