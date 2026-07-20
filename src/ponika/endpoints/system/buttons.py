from pydantic import Field, field_validator

from ponika.endpoints.system.common import ReadUpdateEndpoint
from ponika.endpoints.system.enums import ButtonHandler
from ponika.models import BaseModel, BasePayload


class ButtonBase:
    min: str | None = Field(default=None, min_length=1, max_length=2)
    max: str | None = Field(default=None, min_length=1, max_length=2)
    enabled: bool | None = None

    @field_validator('min', 'max')
    @classmethod
    def validate_press_time(cls, value: str | None) -> str | None:
        if value is not None and (
            not value.isdigit() or not 0 <= int(value) <= 60
        ):
            raise ValueError('button press time must be between 0 and 60')
        return value


class ButtonConfigResponse(BaseModel, ButtonBase):
    id: str
    action: str | None = None
    handler: ButtonHandler | None = None


class ButtonUpdatePayload(BasePayload, ButtonBase):
    id: str


class ButtonsEndpoint(
    ReadUpdateEndpoint[ButtonConfigResponse, ButtonUpdatePayload]
):
    endpoint_path = '/system/buttons/config'
    config_response_model = ButtonConfigResponse
