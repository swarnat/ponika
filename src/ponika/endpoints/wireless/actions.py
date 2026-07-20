from typing import Optional

from pydantic import model_validator

from ponika.endpoints import Endpoint
from ponika.endpoints.wireless.interfaces import (
    WirelessInterfaceConfigResponse,
)
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel, BasePayload


class WirelessScanPayload(BasePayload):
    device: Optional[str] = None


class WirelessJoinPayload(BasePayload):
    device: str
    bssid: Optional[str] = None
    ssid: Optional[str] = None
    password: Optional[str] = None

    @model_validator(mode='after')
    def validate_network_identifier(self) -> 'WirelessJoinPayload':
        if not self.bssid and not self.ssid:
            raise ValueError('either bssid or ssid must be provided')
        return self


class WirelessScanEncryption(BaseModel):
    enabled: bool
    wpa: list[int]
    ciphers: list[str]
    authentication: list[str]


class WirelessScanHtOperation(BaseModel):
    secondary_channel_offset: str
    channel_width: int | float
    primary_channel: int | float


class WirelessScanVhtOperation(BaseModel):
    center_freq_1: int | float
    center_freq_2: int | float
    primary_channel: Optional[int | float] = None
    channel_width: Optional[int | float] = None


class WirelessScanResponse(BaseModel):
    quality_max: int | float
    ssid: str
    bssid: str
    encryption_description: str
    channel: int | float
    mode: str
    quality: int | float
    signal: int | float
    encryption: Optional[WirelessScanEncryption] = None
    ht_operation: Optional[WirelessScanHtOperation] = None
    vht_operation: Optional[WirelessScanVhtOperation] = None


class ActionsEndpoint(Endpoint):
    def scan(self, payload: WirelessScanPayload) -> list[WirelessScanResponse]:
        response = self._client._post_data(
            endpoint='/wireless/actions/scan',
            data_model=list[WirelessScanResponse],
            params=payload,
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def join(
        self, payload: WirelessJoinPayload
    ) -> WirelessInterfaceConfigResponse:
        response = self._client._post_data(
            endpoint='/wireless/actions/join',
            data_model=WirelessInterfaceConfigResponse,
            params=payload,
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data
