from enum import Enum
from typing import Any

from pydantic import Field

from ponika.endpoints import CRUDEndpoint, StatusEndpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel, BasePayload


class InterfaceAreaType(str, Enum):
    LAN = 'lan'
    WAN = 'wan'


class InterfaceMode(str, Enum):
    STATIC = 'static'
    DHCP = 'dhcp'
    STATIC_DHCP = 'static+dhcp'


class InterfaceAuth(str, Enum):
    NONE = 'none'
    PAP = 'pap'
    CHAP = 'chap'


class InterfaceReqAddress(str, Enum):
    TRY = 'try'
    FORCE = 'force'
    NONE = 'none'


class InterfaceReqPrefix(str, Enum):
    AUTO = 'auto'
    NO = 'no'
    PREFIX_48 = '48'
    PREFIX_52 = '52'
    PREFIX_56 = '56'
    PREFIX_60 = '60'
    PREFIX_64 = '64'


class InterfaceMethod(str, Enum):
    NAT = 'nat'
    BRIDGE = 'bridge'
    PASSTHROUGH = 'passthrough'


class InterfacePdpType(str, Enum):
    IP = 'ip'
    IPV6 = 'ipv6'
    IPV4V6 = 'ipv4v6'


class InterfaceIpv6(str, Enum):
    AUTO = 'auto'
    DISABLED = '0'
    ENABLED = '1'


class InterfaceBase:
    name: str | None = None
    enabled: bool | None = None
    proto: str | None = None
    mode: InterfaceMode | None = None
    ipaddr: str | None = None
    netmask: str | None = None
    gateway: str | None = None
    broadcast: str | None = None
    broadcast_dhcp: bool | None = None
    auth: InterfaceAuth | None = None
    username: str | None = None
    password: str | None = None
    ac: str | None = None
    service: str | None = None
    reqaddress: InterfaceReqAddress | None = None
    reqprefix: InterfaceReqPrefix | None = None
    hostname: str | None = None
    method: InterfaceMethod | None = None
    pdptype: InterfacePdpType | None = None
    modem: str | None = None
    sim: str | None = None
    esim_profile: str | None = None
    auto_apn: bool | None = None
    apn: str | None = None
    passthrough_mode: bool | None = None
    framed_routing: str | None = None
    leasetime: str | None = None
    dns: list[str] | None = None
    delegate: bool | None = None
    force_link: bool | None = None
    ipv6: InterfaceIpv6 | None = None
    defaultroute: bool | None = None
    metric: str | None = None
    ip6prefix: str | None = None
    clientid: str | None = None
    vendorid: str | None = None
    keepalive_failure: str | None = None
    keepalive_interval: str | None = None
    host_uniq: str | None = None
    demand: str | None = None
    mac: str | None = None
    macaddr: str | None = None
    mtu: str | None = None
    ip4table: str | None = None
    ip6table: str | None = None
    ip6assign: str | None = None
    ip6hint: str | None = None
    ip6addr: str | None = None
    ip6gw: str | None = None
    ip6ifaceid: str | None = None
    bridge: bool | None = None
    stp: bool | None = None
    igmp_snooping: bool | None = None
    ifname: list[str] | None = None
    fiber_priority: str | None = None
    tag: str | None = None
    priority: str | None = None
    fwzone: str | None = None
    p2p: bool | None = None
    man_vlan: str | None = None
    fallback: bool | None = None
    fallbackip: str | None = None
    device: str | None = None
    vlan_id: str | None = None


class InterfaceConfigResponse(BaseModel, InterfaceBase):
    id: str
    area_type: InterfaceAreaType | None = None
    password_set: bool | None = Field(default=None, alias='password:set')


class InterfaceCreatePayload(BasePayload, InterfaceBase):
    area_type: InterfaceAreaType
    id: str | None = None


class InterfaceUpdatePayload(BasePayload, InterfaceBase):
    id: str


class InterfaceDeleteResponse(BaseModel):
    id: str | None = None


class InterfaceStatusAddress(BaseModel):
    address: str | None = None
    mask: int | None = None


class InterfaceStatusSubdevice(BaseModel):
    rx_bytes: int | None = None
    tx_bytes: int | None = None
    type: str | None = None
    typename: str | None = None
    name: str | None = None
    rx_packets: int | None = None
    tx_packets: int | None = None
    macaddr: str | None = None
    is_up: bool | None = None
    ifname: str | None = None


class InterfaceStatusResponse(BaseModel):
    id: str | None = None
    interface: str | None = None
    name: str | None = None
    ifname: str | None = None
    proto: str | None = None
    type: str | None = None
    typename: str | None = None
    desc: str | None = None
    device: str | None = None
    l3_device: str | None = None
    network_type: str | None = None
    area_type: str | None = None
    rx_bytes: int | None = None
    tx_bytes: int | None = None
    rx_packets: int | None = None
    tx_packets: int | None = None
    metric: int | None = None
    uptime: int | None = None
    up: bool | None = None
    is_up: bool | None = None
    autostart: bool | None = None
    available: bool | None = None
    pending: bool | None = None
    dynamic: bool | None = None
    is_dynamic: bool | None = None
    delegation: bool | None = None
    ipaddrs: list[str] = Field(default_factory=list)
    ip6addrs: list[str] = Field(default_factory=list)
    dns_server: list[str] = Field(default_factory=list, alias='dns-server')
    dns_search: list[Any] = Field(default_factory=list, alias='dns-search')
    dnsaddrs: list[str] = Field(default_factory=list)
    ipv4_address: list[InterfaceStatusAddress] = Field(
        default_factory=list, alias='ipv4-address'
    )
    ipv6_address: list[Any] = Field(default_factory=list, alias='ipv6-address')
    route: list[Any] = Field(default_factory=list)
    subdevices: list[InterfaceStatusSubdevice] = Field(default_factory=list)
    macaddr: str | None = None


class InterfacesEndpoint(
    CRUDEndpoint[
        InterfaceCreatePayload,
        InterfaceConfigResponse,
        InterfaceUpdatePayload,
        InterfaceDeleteResponse,
    ],
    StatusEndpoint[InterfaceStatusResponse],
):
    endpoint_path = '/interfaces/config'
    status_endpoint_path = '/interfaces/status'

    config_response_model = InterfaceConfigResponse
    update_model = InterfaceUpdatePayload
    create_model = InterfaceCreatePayload
    delete_reponse_model = InterfaceDeleteResponse
    status_response_model = InterfaceStatusResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True

    def delete(self, item_id: str | int) -> InterfaceDeleteResponse:
        response = self._client._delete(
            endpoint=f'{self.endpoint_path}/{item_id}',
            data_model=InterfaceDeleteResponse,
        )
        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data or InterfaceDeleteResponse(id=str(item_id))

    def delete_bulk(
        self, item_ids: list[str | int]
    ) -> list[InterfaceDeleteResponse]:
        response = self._client._delete(
            endpoint=self.endpoint_path,
            data_model=InterfaceDeleteResponse,
            params={'data': item_ids},
        )
        if not response.success:
            raise TeltonikaApiException(response.errors)

        return [
            InterfaceDeleteResponse(id=str(item_id)) for item_id in item_ids
        ]
