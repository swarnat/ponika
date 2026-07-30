from typing import Optional

from pydantic import Field, field_validator

from ponika.endpoints import Endpoint
from ponika.endpoints.modems.common import response_data
from ponika.endpoints.modems.enums import (
    BandSelection,
    GsmBand,
    LteBand,
    LteCategory,
    LteNbBand,
    MobileService,
    Nr5gBand,
    Nr5gMode,
    OperatorListMode,
    OperatorSelection,
    SmsLimitPeriod,
    UmtsBand,
    VolteMode,
)
from ponika.models import ApiResponse, BaseModel, BasePayload


class SimCardOptionsBase:
    esim_profile: Optional[str] = None
    modem: Optional[str] = None
    position: Optional[str] = None
    primary: Optional[bool] = None
    deny_roaming: Optional[bool] = None
    volte: Optional[VolteMode] = None
    service: Optional[MobileService] = None
    category_lte: Optional[LteCategory] = None
    nr5g_mode: Optional[Nr5gMode] = None
    pincode: Optional[str] = None
    pukcode: Optional[str] = None
    band: Optional[BandSelection] = None
    gsm: Optional[list[GsmBand]] = None
    umts: Optional[list[UmtsBand]] = None
    lte: Optional[list[LteBand]] = None
    lte_nb: Optional[list[LteNbBand]] = None
    signal_reset_enabled: Optional[bool] = None
    signal_reset_threshold: str
    signal_reset_timeout: str
    operlist: Optional[bool] = None
    opermode: OperatorListMode
    operlist_name: str
    enable_sms_limit: Optional[bool] = None
    sms_limit_num: str
    sms_limit: SmsLimitPeriod
    period: str
    operator: Optional[OperatorSelection] = None
    opernum: Optional[str] = None

    @field_validator('opernum')
    @classmethod
    def validate_operator_number(cls, value: str | None) -> str | None:
        if value is not None and not 5 <= len(value) <= 6:
            raise ValueError('opernum must contain 5 or 6 characters')
        return value


class SimCardConfigResponse(BaseModel, SimCardOptionsBase):
    id: Optional[str] = None
    nr5g: Optional[list[str]] = None
    nr5g_sa: list[str] = Field(default_factory=list)


class SimCardUpdatePayload(BasePayload, SimCardOptionsBase):
    nr5g: Optional[list[Nr5gBand]] = None


class SimCardBulkUpdatePayload(BasePayload, SimCardOptionsBase):
    id: Optional[str] = None
    nr5g: Optional[list[str]] = None
    nr5g_sa: Optional[list[str]] = None


class ModemSimCardsEndpoint(Endpoint):
    def get_config(
        self, modem_id: str, sim_id: str | None = None
    ) -> SimCardConfigResponse | list[SimCardConfigResponse]:
        endpoint = f'/modems/{modem_id}/sim_cards/config'
        if sim_id is not None:
            endpoint = f'{endpoint}/{sim_id}'
            model = SimCardConfigResponse
        else:
            model = list[SimCardConfigResponse]
        response = ApiResponse[model].model_validate(
            self._client._get(endpoint)
        )
        return response_data(response)

    def update(
        self,
        modem_id: str,
        sim_id: str,
        payload: SimCardUpdatePayload,
    ) -> SimCardConfigResponse:
        response = self._client._put_data(
            endpoint=f'/modems/{modem_id}/sim_cards/config/{sim_id}',
            data_model=SimCardConfigResponse,
            params=payload,
        )
        return response_data(response)

    def update_bulk(
        self, modem_id: str, payloads: list[SimCardBulkUpdatePayload]
    ) -> list[SimCardConfigResponse]:
        response = self._client._put(
            endpoint=f'/modems/{modem_id}/sim_cards/config',
            data_model=list[SimCardConfigResponse],
            params={'data': [payload.asdict() for payload in payloads]},
        )
        return response_data(response)
