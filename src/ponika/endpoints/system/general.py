from ponika.endpoints.system.common import ReadUpdateEndpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload


class GeneralConfigBase:
    lang_code: str | None = None
    advanced: bool | None = None
    devicename: str | None = None
    hostname: str | None = None
    notifications_enabled: bool | None = None
    alerts_enabled: bool | None = None
    api_session_timeout: str | None = None
    session_timeout: str | None = None


class GeneralConfigResponse(BaseModel, GeneralConfigBase):
    id: str | None = None
    firstlogin: bool | None = None


class GeneralUpdatePayload(BasePayload, GeneralConfigBase):
    id: str


class LanguageOption(BaseModel):
    name: str | None = None
    code: str | None = None
    filename: str | None = None


class GeneralEndpoint(
    ReadUpdateEndpoint[GeneralConfigResponse, GeneralUpdatePayload]
):
    endpoint_path = '/system/config'
    config_response_model = GeneralConfigResponse

    def get_languages(self) -> list[LanguageOption]:
        response = ApiResponse[list[LanguageOption]].model_validate(
            self._client._get('/system/languages/options')
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)
        return response.data
