from ponika.endpoints.system.common import ReadUpdateEndpoint
from ponika.models import BaseModel, BasePayload


class LedBase:
    enabled: bool | None = None


class LedConfigResponse(BaseModel, LedBase):
    id: str


class LedUpdatePayload(BasePayload, LedBase):
    id: str


class LedEndpoint(ReadUpdateEndpoint[LedConfigResponse, LedUpdatePayload]):
    endpoint_path = '/system/led/config'
    config_response_model = LedConfigResponse
