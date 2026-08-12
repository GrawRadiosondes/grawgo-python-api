from faker import Faker
from requests import codes

from grawgo.api import Api


def test_user_self(api_as_api: Api):
    assert api_as_api.user_self().status_code == codes.ok


def test_user_self_first_station(api_as_api: Api):
    assert api_as_api.user_self_first_station()


def test_create_flight(api_as_api: Api, faker: Faker):
    assert (
        api_as_api.create_flight(
            station_id=api_as_api.user_self_first_station()["data"]["id"],
            status="created",
            sonde_serial=faker.name(),
            set_frequency=faker.random_int(min=400, max=406),
            sonde_firmware_version=faker.name(),
        ).status_code
        == codes.created
    )


def test_ascend_flight(api_as_api: Api, faker: Faker):
    flight_id = api_as_api.create_flight(
        station_id=api_as_api.user_self_first_station()["data"]["id"],
        status="created",
        sonde_serial=faker.name(),
        set_frequency=faker.random_int(min=400, max=406),
        sonde_firmware_version=faker.name(),
    ).json()["data"]["id"]

    assert api_as_api.ascend_flight(flight_id=flight_id).status_code == codes.ok


def test_create_measurement(api_as_api: Api, faker: Faker):
    assert (
        api_as_api.create_measurement(
            flight_id=api_as_api.create_flight(
                station_id=api_as_api.user_self_first_station()["data"]["id"],
                status="created",
                sonde_serial=faker.name(),
                set_frequency=faker.random_int(min=400, max=406),
                sonde_firmware_version=faker.name(),
            ).json()["data"]["id"],
            time_after_launch=0,
            utc_time="00:00:00",
            pressure=0,
            temperature=0,
            humidity=0,
            wind_speed=0,
            wind_direction=0,
            latitude=0,
            longitude=0,
            altitude=0,
            vertical_speed=0,
            geo_potential=0,
            dew_point=0,
            elevation=0,
            azimuth=0,
            distance=0,
        ).status_code
        == codes.created
    )
