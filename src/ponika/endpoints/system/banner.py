from pydantic import Field

from ponika.endpoints.system.common import ReadUpdateEndpoint
from ponika.models import BaseModel, BasePayload


class BannerBase:
    enabled: bool | None = None
    title: str | None = Field(default=None, max_length=64)
    message: str | None = Field(default=None, max_length=512)


class BannerConfigResponse(BaseModel, BannerBase):
    id: str


class BannerUpdatePayload(BasePayload, BannerBase):
    id: str


class BannerEndpoint(
    ReadUpdateEndpoint[BannerConfigResponse, BannerUpdatePayload]
):
    endpoint_path = '/system/banner/config'
    config_response_model = BannerConfigResponse
