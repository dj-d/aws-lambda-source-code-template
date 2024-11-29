import os

TARGET_ROLE_NAME = str(os.getenv(
    key='TARGET_ROLE_NAME'
))

TARGET_ACCOUNT_ID = str(os.getenv(
    key='TARGET_ACCOUNT_ID',
    default='315237124572'
))