import pytest
from faker import Faker
from requests import codes

from grawgo.api import Api


def test_user_self(api_as_admin: Api):
    assert api_as_admin.user_self().status_code == codes.ok


def test_user_self_stations(api_as_admin: Api):
    assert isinstance(api_as_admin.user_self_stations(), list)


@pytest.mark.parametrize("role", ["admin", "station_admin", "user", "api"])
def test_create_user(api_as_admin: Api, faker: Faker, role: str):
    assert (
        api_as_admin.create_user(
            faker.email(),
            faker.password(),
            role,
            faker.name(),
        ).status_code
        == codes.created
    )


@pytest.mark.parametrize("type", ["selerys", "operated_fixed", "operated_mobile"])
def test_create_station(api_as_admin: Api, faker: Faker, type: str):
    assert (
        api_as_admin.create_station(
            faker.name(),
            type,
            faker.random_int(10000, 99999),
            float(faker.latitude()),
            float(faker.longitude()),
            faker.random_int(min=0, max=8848),
        ).status_code
        == codes.created
    )


@pytest.mark.parametrize("role", ["admin", "station_admin", "user", "api"])
@pytest.mark.parametrize("type", ["selerys", "operated_fixed", "operated_mobile"])
def test_attach_station_to_user(api_as_admin: Api, faker: Faker, role: str, type: str):
    username = faker.email()
    password = faker.password()
    user = api_as_admin.create_user(username, password, role, faker.name()).json()
    user_api = Api(api_as_admin.base_url, username, password)

    assert len(user_api.user_self_stations()) == 0

    station = api_as_admin.create_station(
        faker.name(),
        type,
        faker.random_int(10000, 99999),
        float(faker.latitude()),
        float(faker.longitude()),
        faker.random_int(min=0, max=8848),
    ).json()
    assert (
        api_as_admin.attach_station_to_user(
            user["data"]["id"], station["data"]["id"]
        ).status_code
        == codes.ok
    )

    stations = user_api.user_self_stations()
    assert len(stations) == 1
    assert station == stations[0]
