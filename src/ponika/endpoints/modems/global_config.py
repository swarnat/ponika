from typing import Optional

from ponika.endpoints import Endpoint
from ponika.endpoints.modems.common import response_data
from ponika.models import ApiResponse, BaseModel, BasePayload


class ModemGlobalConfigResponse(BaseModel):
    modem: Optional[str] = None
    flight_mode: Optional[bool] = None


class ModemGlobalConfigUpdatePayload(BasePayload):
    modem: Optional[str] = None
    flight_mode: Optional[bool] = None


class ModemGlobalConfigEndpoint(Endpoint):
    def get(self, modem_id: str) -> ModemGlobalConfigResponse:
        response = self._client._get(f'/modems/{modem_id}/global')
        return response_data(
            ApiResponse[ModemGlobalConfigResponse].model_validate(response)
        )

    def update(
        self, modem_id: str, payload: ModemGlobalConfigUpdatePayload
    ) -> ModemGlobalConfigResponse:
        response = self._client._put_data(
            endpoint=f'/modems/{modem_id}/global',
            data_model=ModemGlobalConfigResponse,
            params=payload,
        )
        return response_data(response)
