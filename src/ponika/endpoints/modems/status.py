from typing import Any, Optional, overload

from pydantic import Field, TypeAdapter

from ponika.endpoints import Endpoint
from ponika.endpoints.modems.common import response_data
from ponika.endpoints.modems.enums import (
    ApnAuthentication,
    ConnectionState,
    ConnectionStateId,
    MobileStage,
    ModemMode,
    ModemName,
    ModemStateId,
    NetworkType,
    OperatorStatus,
    PdpType,
    PinState,
    PinStateId,
    RegistrationState,
    RegistrationStateId,
    SecondaryCarrierBandState,
    SimState,
    SimStateId,
)
from ponika.models import ApiResponse, BaseModel


class ModemCellInfo(BaseModel):
    mcc: Optional[str] = None
    mnc: Optional[str] = None
    cellid: Optional[str] = None
    ue_state: Optional[int] = None
    lac: Optional[str] = None
    tac: Optional[str] = None
    pcid: Optional[int] = None
    earfcn: Optional[int] = None
    arfcn: Optional[str] = None
    uarfcn: Optional[str] = None
    nr_arfcn: Optional[str] = Field(default=None, alias='nr-arfcn')
    rsrp: Optional[str] = None
    rsrq: Optional[str] = None
    sinr: Optional[int | float | str] = None
    bandwidth: Optional[str] = None


class ModemCarrierAggregationSignal(BaseModel):
    band: Optional[str] = None
    bandwidth: Optional[str] = None
    sinr: Optional[int | float] = None
    rsrq: Optional[int | float] = None
    rsrp: Optional[int | float] = None
    pcid: Optional[int] = None
    frequency: Optional[int | float] = None


class ModemOnlineStatus(BaseModel):
    id: str
    imei: Optional[str] = None
    model: Optional[str] = None
    cell_info: list[ModemCellInfo] = Field(default_factory=list)
    dynamic_mtu: Optional[bool] = None
    service_modes: dict[str, list[str]] = Field(default_factory=dict)
    lac: Optional[str] = None
    tac: Optional[str] = None
    name: Optional[ModemName] = None
    index: Optional[int] = None
    sim_count: Optional[int] = None
    version: Optional[str] = None
    cfg_version: Optional[str] = None
    serial: Optional[str] = None
    manufacturer: Optional[str] = None
    builtin: Optional[bool] = None
    mode: Optional[ModemMode] = None
    primary: Optional[int] = None
    multi_apn: Optional[bool] = None
    ipv6: Optional[bool] = None
    volte_supported: Optional[bool] = None
    auto_2g_bands: Optional[bool] = None
    auto_3g_bands: Optional[bool] = None
    operators_scan: Optional[bool] = None
    mobile_dfota: Optional[bool] = None
    no_ussd: Optional[bool] = None
    framed_routing: Optional[bool] = None
    low_signal_reconnect: Optional[bool] = None
    active_sim: Optional[int] = None
    conntype: Optional[str] = None
    simstate: Optional[SimState] = None
    simstate_id: Optional[SimStateId] = None
    data_conn_state: Optional[ConnectionState] = None
    state: Optional[ConnectionState] = None
    data_conn_state_id: Optional[ConnectionStateId] = None
    state_id: Optional[ConnectionStateId] = None
    txbytes: Optional[int] = None
    rxbytes: Optional[int] = None
    baudrate: Optional[int] = None
    is_busy: Optional[int] = None
    data_off: Optional[bool] = None
    busy_state: Optional[str] = None
    busy_state_id: Optional[int] = None
    pinstate: Optional[PinState] = None
    pinstate_id: Optional[PinStateId] = None
    operator_state: Optional[RegistrationState] = None
    netstate: Optional[RegistrationState] = None
    operator_state_id: Optional[RegistrationStateId] = None
    netstate_id: Optional[RegistrationStateId] = None
    rssi: Optional[int | float] = None
    signal: Optional[int | float] = None
    operator: Optional[str] = None
    oper: Optional[str] = None
    provider: Optional[str] = None
    ntype: Optional[str] = None
    imsi: Optional[str] = None
    iccid: Optional[str] = None
    cellid: Optional[str] = None
    rscp: Optional[str] = None
    ecio: Optional[str] = None
    rsrp: Optional[int | float] = None
    rsrq: Optional[int | float] = None
    sinr: Optional[int | float] = None
    pinleft: Optional[int] = None
    pukleft: Optional[int] = None
    volte: Optional[bool] = None
    sc_band_av: Optional[SecondaryCarrierBandState] = None
    ca_signal: list[ModemCarrierAggregationSignal] = Field(
        default_factory=list
    )
    temperature: Optional[int | float] = None
    esim_profile: Optional[str] = None
    sim_switch_enabled: Optional[bool] = None
    mobile_stage: Optional[MobileStage] = None
    gnss_state: Optional[int] = None
    modem_state_id: Optional[ModemStateId] = None
    band: Optional[str] = None
    wwan_gnss_conflict: Optional[bool] = None
    auto_5g_mode: Optional[bool] = None
    csd: Optional[bool] = None
    nr5g_sa_disabled: Optional[bool] = None
    esim_bootstrap: Optional[bool] = None


class ModemOfflineStatus(BaseModel):
    id: str
    name: Optional[ModemName] = None
    offline: Optional[bool] = None
    blocked: Optional[bool] = None
    disabled: Optional[bool] = None
    builtin: Optional[bool] = None
    primary: Optional[bool] = None
    sim_count: Optional[int] = None
    csd: Optional[bool] = None
    mode: Optional[ModemMode] = None
    multi_apn: Optional[bool] = None
    operators_scan: Optional[bool] = None
    dynamic_mtu: Optional[bool] = None
    ipv6: Optional[bool] = None
    volte: Optional[bool] = None
    esim_profile: Optional[str] = None
    sim_switch_enabled: Optional[bool] = None
    modem_state_id: Optional[ModemStateId] = None


ModemStatus = ModemOnlineStatus | ModemOfflineStatus
MODEM_STATUS_OFFLINE_FIELDS = frozenset({'offline', 'blocked', 'disabled'})
MODEM_STATUS_ADAPTERS = {
    True: TypeAdapter(ModemOfflineStatus),
    False: TypeAdapter(ModemOnlineStatus),
}


def parse_modem_status(data: Any) -> ModemStatus:
    """Parse status without allowing a failed online model to become offline."""
    if not isinstance(data, dict):
        return TypeAdapter(ModemStatus).validate_python(data)

    is_offline = bool(MODEM_STATUS_OFFLINE_FIELDS.intersection(data))
    return MODEM_STATUS_ADAPTERS[is_offline].validate_python(data)


class ModemApnStatus(BaseModel):
    id: Optional[int] = None
    password: str
    apn: str
    user: str
    carrier: str
    auth: ApnAuthentication
    pdptype: PdpType


class ModemApnsStatus(BaseModel):
    modem: Optional[str] = None
    apns: list[ModemApnStatus] = Field(default_factory=list)


class ModemStatusError(BaseModel):
    code: int
    error: str
    modem: str


class ModemSignalStatus(BaseModel):
    timestamp: str
    network_type: NetworkType
    band: str
    channel_number: Optional[int | float] = None
    sinr: Optional[int | float] = None
    rssi: Optional[int | float] = None
    ecio: Optional[int | float] = None
    rsrp: Optional[int | float] = None
    rsrq: Optional[int | float] = None


class ModemSignalsStatus(BaseModel):
    modem: Optional[str] = None
    signal: list[ModemSignalStatus] = Field(default_factory=list)


class ModemOperator(BaseModel):
    net_access_type: Optional[str] = None
    status_code: Optional[int] = None
    status: Optional[OperatorStatus] = None
    op_name: Optional[str] = None
    short_name: Optional[str] = None
    num_name: Optional[str] = None


class ModemScanStatus(BaseModel):
    last_scan: Optional[str] = None
    operators: list[ModemOperator] = Field(default_factory=list)


class ModemScansStatus(ModemScanStatus):
    modem: Optional[str] = None


class ModemCountryStatus(BaseModel):
    mcc: Optional[str] = None
    country: Optional[str] = None


class ModemStatusEndpoint(Endpoint):
    @overload
    def get_status(self, modem_id: str) -> ModemStatus: ...

    @overload
    def get_status(self) -> list[ModemStatus]: ...

    def get_status(
        self, modem_id: str | None = None
    ) -> ModemStatus | list[ModemStatus]:
        endpoint = '/modems/status'
        if modem_id is not None:
            endpoint = f'{endpoint}/{modem_id}'

        response = ApiResponse[Any].model_validate(self._client._get(endpoint))
        data = response_data(response)
        if modem_id is not None:
            return parse_modem_status(data)
        if not isinstance(data, list):
            return TypeAdapter(list[ModemStatus]).validate_python(data)
        return [parse_modem_status(item) for item in data]

    def get_apns(
        self, modem_id: str | None = None
    ) -> list[ModemApnStatus] | list[ModemApnsStatus | ModemStatusError]:
        endpoint = '/modems/apns/status'
        if modem_id is not None:
            endpoint = f'{endpoint}/{modem_id}'
            model = list[ModemApnStatus]
        else:
            model = list[ModemApnsStatus | ModemStatusError]
        response = ApiResponse[model].model_validate(
            self._client._get(endpoint)
        )
        return response_data(response)

    def get_signal(
        self, modem_id: str | None = None
    ) -> list[ModemSignalStatus] | list[ModemSignalsStatus | ModemStatusError]:
        endpoint = '/modems/signal/status'
        if modem_id is not None:
            endpoint = f'{endpoint}/{modem_id}'
            model = list[ModemSignalStatus]
        else:
            model = list[ModemSignalsStatus | ModemStatusError]
        response = ApiResponse[model].model_validate(
            self._client._get(endpoint)
        )
        return response_data(response)

    def get_scan(
        self, modem_id: str | None = None
    ) -> ModemScanStatus | list[ModemScansStatus]:
        endpoint = '/modems/scan/status'
        model = ModemScanStatus
        if modem_id is not None:
            endpoint = f'{endpoint}/{modem_id}'
        else:
            model = list[ModemScansStatus]
        response = ApiResponse[model].model_validate(
            self._client._get(endpoint)
        )
        return response_data(response)

    def get_countries(self) -> list[ModemCountryStatus]:
        response = ApiResponse[list[ModemCountryStatus]].model_validate(
            self._client._get('/modems/countries/status')
        )
        return response_data(response)
