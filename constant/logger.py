import os

DEBUG_MODE = bool(os.getenv(
    key='DEBUG_MODE',
    default='false').lower() == 'true'
)

VERBOSE_MODE = bool(os.getenv(
    key='VERBOSE_MODE',
    default='false').lower() == 'true'
)
