import logging
from os import getenv

logging.basicConfig(
    level=getattr(
        logging, getenv(key="LOG_LEVEL", default="INFO").upper(), logging.INFO
    ),
    format="%(levelname)s: %(message)s",
)
