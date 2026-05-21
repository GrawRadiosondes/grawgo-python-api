from logging import error
from os import getenv
from os.path import dirname, isfile, join

import pytest
from dotenv import load_dotenv
from faker import Faker

from grawgo.api import Api


def load_env():
    env_file = join(dirname(__file__), "../.env")

    if not isfile(env_file):
        error("script can not start because .env file is missing")
        exit(1)

    load_dotenv(env_file)


@pytest.fixture(scope="session")
def api_as_public():
    load_env()
    return Api(
        base_url=getenv("GG_API_URL") or "https://localhost/api",
    )


@pytest.fixture(scope="session")
def api_as_admin():
    load_env()
    return Api(
        getenv("GG_API_URL") or "https://localhost/api",
        getenv("GG_ADMIN_USERNAME") or "admin@domain.tld",
        getenv("GG_ADMIN_PASSWORD") or "password",
    )


@pytest.fixture(scope="session")
def api_as_api():
    load_env()
    return Api(
        getenv("GG_API_URL") or "https://localhost/api",
        getenv("GG_API_USERNAME") or "admin@domain.tld",
        getenv("GG_API_PASSWORD") or "password",
    )


@pytest.fixture(scope="session")
def faker() -> Faker:
    return Faker()
