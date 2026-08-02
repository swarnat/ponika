from ponika.endpoints import Endpoint
from pydantic import Field
from ponika.endpoints.system.enums import DeviceParameterType
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel


class ManufacturingInfo(BaseModel):
    macEth: str | None = None
    name: str | None = None
    hwver: str | None = None
    batch: str | None = None
    serial: str | None = None
    mac: str | None = None
    blver: str | None = None
    branch: str | None = None
    sim1_boot_iccid: str | None = None
    sim2_boot_iccid: str | None = None
    sim3_boot_iccid: str | None = None
    sim4_boot_iccid: str | None = None


class DevicePort(BaseModel):
    name: str | None = None
    position: int | str | None = None
    num: int | str | None = None
    mac: str | None = None


class SystemRelease(BaseModel):
    distribution: str | None = None
    revision: str | None = None
    version: str | None = None
    target: str | None = None
    description: str | None = None


class StaticSystemInfo(BaseModel):
    fw_version: str | None = None
    kernel: str | None = None
    system: str | None = None
    device_name: str | None = None
    hostname: str | None = None
    cpu_count: float | None = None
    release: SystemRelease | None = None
    fw_build_date: str | None = None
    model: str | None = None
    board_name: str | None = None


class DeviceFeatures(BaseModel):
    ipv6: bool | None = None


class BoardModem(BaseModel):
    id: str | None = None
    num: str | None = None
    builtin: bool | None = None
    simcount: float | None = None
    gps_out: bool | None = None
    primary: bool | None = None
    revision: str | None = None
    modem_func_id: float | None = None
    multi_apn: bool | None = None
    operator_scan: bool | None = None
    dhcp_filter: bool | None = None
    dynamic_mtu: bool | None = None
    ipv6: bool | None = None
    volte: bool | None = None
    csd: bool | None = None
    band_list: list[str] | None = None
    product: str | None = None
    vendor: str | None = None
    gps: str | None = None
    stop_bits: str | None = None
    boudrate: str | None = None
    type: str | None = None
    desc: str | None = None
    control: str | None = None


class BoardSerial(BaseModel):
    path: str | None = None
    parity_types: list[str] | None = None
    stop_bits: list[str] | None = None
    bauds: list[str] | None = None
    data_bits: list[str] | None = None
    flow_control: list[str] | None = None
    devices: list[str] | None = None
    external_devices: list[str] | None = None


class BoardNetworkInterface(BaseModel):
    proto: str | None = None
    device: str | None = None
    ports: list[str] | None = None
    default_ip: str | None = None


class BoardNetwork(BaseModel):
    wan: BoardNetworkInterface | None = None
    lan: BoardNetworkInterface | None = None


class BoardModel(BaseModel):
    id: str | None = None
    platform: str | None = None
    name: str | None = None


class BoardNetworkOptions(BaseModel):
    readonly_vlans: float | None = None
    ula: bool | None = None
    disable_vlan: bool | None = None
    no_metric: bool | None = None
    max_mtu: float | None = None
    vlans: float | None = None


class SwitchRole(BaseModel):
    ports: str | None = None
    role: str | None = None
    device: str | None = None


class SwitchPort(BaseModel):
    device: str | None = None
    num: float | None = None
    want_untag: bool | None = None
    need_tag: bool | None = None
    role: str | None = None
    index: float | None = None


class BoardSwitch(BaseModel):
    enable: bool | None = None
    roles: list[SwitchRole] | None = None
    ports: list[SwitchPort] | None = None
    reset: bool | None = None


class BoardSwitches(BaseModel):
    switch0: BoardSwitch | None = None


class BoardHardwareInfo(BaseModel):
    wps: bool | None = None
    rs232: bool | None = None
    nat_offloading: bool | None = None
    dual_sim: bool | None = None
    bluetooth: bool | None = None
    soft_port_mirror: bool | None = None
    vcert: bool | None = None
    micro_usb: bool | None = None
    wifi: bool | None = None
    sd_card: bool | None = None
    multi_tag: bool | None = None
    dual_modem: bool | None = None
    sfp_switch: bool | None = None
    dsa: bool | None = None
    hw_nat: bool | None = None
    sw_rst_on_init: bool | None = None
    at_sim: bool | None = None
    port_link: bool | None = None
    ios: bool | None = None
    usb: bool | None = None
    console: bool | None = None
    dual_band_ssid: bool | None = None
    gps: bool | None = None
    ethernet: bool | None = None
    sfp_port: bool | None = None
    rs485: bool | None = None
    mobile: bool | None = None
    poe: bool | None = None
    gigabit_port: bool | None = None
    two_5_gigabit_port: bool | None = Field(
        default=None, alias='2_5_gigabit_port'
    )


class BoardInfo(BaseModel):
    modems: list[BoardModem] | None = None
    serial: list[BoardSerial] | None = None
    network: BoardNetwork | None = None
    model: BoardModel | None = None
    usb_jack: str | None = None
    network_options: BoardNetworkOptions | None = None
    switch: BoardSwitches | None = None
    hwinfo: BoardHardwareInfo | None = None


class DeviceStatusResponse(BaseModel):
    mnfinfo: ManufacturingInfo | None = None
    ports: list[DevicePort] | None = None
    static: StaticSystemInfo | None = None
    features: DeviceFeatures | None = None
    board: BoardInfo | None = None


class DeviceMemoryUsage(BaseModel):
    ram_buffered: float | None = None
    ram_total: float | None = None
    ram_used: float | None = None
    flash_total: float | None = None
    ram_free: float | None = None
    flash_free: float | None = None
    flash_percentage: float | None = None
    flash_used: float | None = None
    ram_percentage: float | None = None
    ram_shared: float | None = None


class DeviceLoadUsage(BaseModel):
    min5: float | None = None
    min15: float | None = None
    min1: float | None = None


class DeviceUsageStatusResponse(BaseModel):
    memory: DeviceMemoryUsage | None = None
    uptime: str | None = None
    loadavg: float | None = None
    localtime: float | None = None
    load: DeviceLoadUsage | None = None
    uptime_seconds: float | None = None


class DeviceParameter(BaseModel):
    type: DeviceParameterType
    description: str
    id: str
    io_name: str | None = None
    block_pins: list[int] | None = None


class DeviceEndpoint(Endpoint):
    def get_status(self) -> DeviceStatusResponse:
        return self._get('/system/device/status', DeviceStatusResponse)

    def get_usage_status(self) -> DeviceUsageStatusResponse:
        return self._get(
            '/system/device/usage/status', DeviceUsageStatusResponse
        )

    def get_load_status(self) -> list[list[float]]:
        return self._get('/system/device/load/status', list[list[float]])

    def get_packages_status(self) -> list[str]:
        return self._get('/system/device/packages/status', list[str])

    def get_parameters_status(self) -> list[DeviceParameter]:
        return self._get(
            '/system/device/parameters/status', list[DeviceParameter]
        )

    def _get(self, endpoint: str, data_model):
        response = ApiResponse[data_model].model_validate(
            self._client._get(endpoint)
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)
        return response.data
