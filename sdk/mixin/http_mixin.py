import base64
import hmac
import json
from typing import Optional

import requests

from sdk.glassbox_config import GlassBoxConfig, HMACCredentials, JWTCredentials


class HttpMixin:
    config: GlassBoxConfig

    def hmac(self, key: str, message: str):
        _hmac = hmac.new(key=key.encode(), digestmod="sha256")
        _hmac.update(bytes(message, encoding="utf-8"))
        return base64.b64encode(_hmac.digest()).decode()

    # noinspection PyMethodMayBeStatic
    def to_json(self, obj: dict):
        return json.dumps(obj, separators=(",", ":"))

    def http_put(self, path: str, data: {}, authorized: bool = True) -> Optional[dict]:
        message = self.to_json(data)

        headers = {"Content-Type": "application/json"}
        if authorized:
            headers["Authorization"] = self._get_token(message)

        text = requests.put(self.config.url + "/" + path, data=message, headers=headers).text
        response = json.loads(text) if len(text) > 0 else None
        if response is not None and "errorMessage" in response:
            raise ValueError(response["errorMessage"])

        return response

    def http_post(self, path: str, data: {}):
        message = self.to_json(data)

        headers = {
            "Content-Type": "application/json",
            "Authorization": self._get_token(message)
        }
        text = requests.post(self.config.url + "/" + path, data=message, headers=headers).text
        response = json.loads(text) if len(text) > 0 else None
        if response is not None and "errorMessage" in response:
            raise ValueError(response["errorMessage"])

        return response

    def _get_token(self, message):
        credentials = self.config.credentials
        if isinstance(credentials, HMACCredentials):
            return "HMAC " + credentials.api_key + ":" + self.hmac(credentials.api_secret, message)

        if isinstance(credentials, JWTCredentials):
            jwt = self.http_put("signin", {
                "username": credentials.username,
                "password": credentials.password
            }, authorized=False)
            return "Bearer " + jwt["idToken"]

        raise ValueError("invalid credentials")
