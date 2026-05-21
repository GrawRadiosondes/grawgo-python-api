from logging import info
from typing import Any
from urllib.parse import urlparse

from requests import Response, get, post


class Api:
    def __init__(
        self,
        base_url: str,
        username: str = "",
        password: str = "",
        logging: bool = False,
    ) -> None:
        self.base_url: str = base_url
        self.auth: tuple[str, str] = (username, password)
        self.logging: bool = logging
        self.verify_https: bool = urlparse(self.base_url).hostname != "localhost"

    def log(self, message: str | dict[str, Any]) -> None:
        if self.logging:
            if isinstance(message, dict) and "password" in message:
                message = {**message, "password": "[REDACTED]"}

            info(msg=message)

    def log_response(self, response: Response) -> None:
        if self.logging and not response.ok:
            info(msg=response.status_code)
            info(msg=response.content)

    def get(self, path: str, authorized: bool = True) -> Response:
        self.log(message=f"GET {self.base_url}/{path}")

        auth = None
        if authorized:
            auth = self.auth

        response: Response = get(
            url=f"{self.base_url}/{path}",
            headers={
                "Accept": "application/json",
            },
            auth=auth,
            verify=self.verify_https,
        )

        self.log_response(response=response)
        return response

    def post(self, path: str, json: Any) -> Response:
        # TODO: fix for list in json instead of dict
        # sanitized_json: dict[str, Any] = {**json}
        # if "password" in sanitized_json:
        #    sanitized_json["password"] = "[REDACTED]"
        # self.log(message=f"POST {self.base_url}/{path} {sanitized_json}")

        response: Response = post(
            url=f"{self.base_url}/{path}",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=self.auth,
            json=json,
            verify=self.verify_https,
        )

        self.log_response(response=response)
        return response

    def status(self) -> Response:
        return self.get(path="status", authorized=False)

    def user_self(self) -> Response:
        return self.get(path="user/self")

    def user_self_stations(self) -> list[Any]:
        return self.user_self().json()["data"]["stations"]

    def user_self_first_station(self):
        return self.user_self_stations()[0]

    def create_user(self, email: str, password: str, role: str, name: str) -> Response:
        return self.post(
            path="user",
            json={
                "email": email,
                "password": password,
                "role": role,
                "name": name,
            },
        )

    def create_station(
        self,
        name: str,
        operation_type: str,
        wmo_id: int,
        latitude: float,
        longitude: float,
        altitude: float,
    ) -> Response:
        return self.post(
            path="station",
            json={
                "name": name,
                "type": operation_type,
                "wmo_id": wmo_id,
                "latitude": latitude,
                "longitude": longitude,
                "altitude": altitude,
            },
        )

    def create_flight(
        self,
        station_id: int,
        status: str,
        sonde_serial: str,
        set_frequency: float,
        sonde_firmware_version: str,
    ) -> Response:
        return self.post(
            path="flight",
            json={
                "station_id": station_id,
                "status": status,
                "sonde_serial": sonde_serial,
                "set_frequency": set_frequency,
                "sonde_firmware_version": sonde_firmware_version,
            },
        )

    def create_measurement(
        self,
        flight_id: int,
        time_after_launch: int,
        utc_time: str,
        pressure: float,
        temperature: float,
        humidity: float,
        wind_speed: float,
        wind_direction: float,
        latitude: float,
        longitude: float,
        altitude: float,
        vertical_speed: float,
        geo_potential: float,
        dew_point: float,
        elevation: float,
        azimuth: float,
        distance: float,
    ) -> Response:
        return self.post(
            path="measurement",
            json=[
                {
                    "flight_id": flight_id,
                    "time_after_launch": time_after_launch,
                    "utc_time": utc_time,
                    "pressure": pressure,
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "wind_direction": wind_direction,
                    "latitude": latitude,
                    "longitude": longitude,
                    "altitude": altitude,
                    "vertical_speed": vertical_speed,
                    "geo_potential": geo_potential,
                    "dew_point": dew_point,
                    "elevation": elevation,
                    "azimuth": azimuth,
                    "distance": distance,
                },
            ],
        )

    def attach_station_to_user(self, user_id: int, station_id: int) -> Response:
        return self.post(path=f"user/{user_id}/attachStation/{station_id}", json={})
