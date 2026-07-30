from typing import Optional

from pydantic import Field

from ponika.endpoints import Endpoint
from ponika.endpoints.modems.common import (
    EmptyModemActionResponse,
    ensure_success,
    response_data,
)
from ponika.endpoints.modems.enums import OperatorStatus, UssdState
from ponika.models import BaseModel, BasePayload


class SendUssdPayload(BasePayload):
    ussd: str


class SendUssdResponse(BaseModel):
    response: Optional[str] = None
    message: Optional[str] = None
    coding_scheme: Optional[int | float] = None
    state_id: Optional[UssdState] = None
    timestamp: Optional[int | float] = None


class ExecAtPayload(BasePayload):
    command: str


class ExecAtResponse(BaseModel):
    response: Optional[str] = None


class ScanNetworkResponse(BaseModel):
    net_access_type: str
    status_code: int
    status: OperatorStatus
    op_name: str
    short_name: str
    num_name: str


class SimUnblockPayload(BasePayload):
    pin: str
    puk: str


class SimUnblockResponse(BaseModel):
    pin_set: Optional[bool] = Field(default=None, alias='pin:set')


class SimUnlockPayload(BasePayload):
    pin: str


class ChangePinPayload(BasePayload):
    pin: str
    new_pin: str


class ChangePinResponse(BaseModel):
    new_pin_set: Optional[bool] = Field(default=None, alias='new_pin:set')


class PinLockPayload(BasePayload):
    enabled: bool
    pin: str


class ModemActionsEndpoint(Endpoint):
    def send_ussd(
        self, modem_id: str, payload: SendUssdPayload
    ) -> SendUssdResponse:
        return response_data(
            self._client._post_data(
                endpoint=f'/modems/{modem_id}/actions/send_ussd',
                data_model=SendUssdResponse,
                params=payload,
            )
        )

    def scan_network(self, modem_id: str) -> list[ScanNetworkResponse]:
        return response_data(
            self._client._post(
                endpoint=f'/modems/{modem_id}/actions/scan_network',
                data_model=list[ScanNetworkResponse],
            )
        )

    def reboot(self, modem_id: str) -> None:
        self._empty_action(modem_id, 'reboot')

    def exec_at(self, modem_id: str, payload: ExecAtPayload) -> ExecAtResponse:
        return response_data(
            self._client._post_data(
                endpoint=f'/modems/{modem_id}/actions/exec_at',
                data_model=ExecAtResponse,
                params=payload,
            )
        )

    def restart_connection(self, modem_id: str) -> None:
        self._empty_action(modem_id, 'restart_connection')

    def sim_unblock(
        self, modem_id: str, payload: SimUnblockPayload
    ) -> SimUnblockResponse:
        return response_data(
            self._client._post_data(
                endpoint=f'/modems/{modem_id}/actions/sim_unblock',
                data_model=SimUnblockResponse,
                params=payload,
            )
        )

    def sim_unlock(self, modem_id: str, payload: SimUnlockPayload) -> None:
        self._payload_action(modem_id, 'sim_unlock', payload)

    def change_pin(
        self, modem_id: str, payload: ChangePinPayload
    ) -> ChangePinResponse:
        return response_data(
            self._client._post_data(
                endpoint=f'/modems/{modem_id}/actions/change_pin',
                data_model=ChangePinResponse,
                params=payload,
            )
        )

    def pin_lock(self, modem_id: str, payload: PinLockPayload) -> None:
        self._payload_action(modem_id, 'pin_lock', payload)

    def _empty_action(self, modem_id: str, action: str) -> None:
        response = self._client._post(
            endpoint=f'/modems/{modem_id}/actions/{action}',
            data_model=EmptyModemActionResponse,
        )
        ensure_success(response)

    def _payload_action(
        self, modem_id: str, action: str, payload: BasePayload
    ) -> None:
        response = self._client._post_data(
            endpoint=f'/modems/{modem_id}/actions/{action}',
            data_model=EmptyModemActionResponse,
            params=payload,
        )
        ensure_success(response)
