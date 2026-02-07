from dataclasses import dataclass, field
from ponika.exceptions import TeltonikaApiException
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, List, Optional

from ponika.models import ApiResponse, BasePayload

from ponika.endpoints.wireless.enums import Encryption, Cipher, WifiMode

if TYPE_CHECKING:
    from ponika import PonikaClient

@dataclass
class WirelessInterfaceDefinition(BasePayload):
    id: Optional[str] = None
    key_set: Optional[str] = None
    auth_secret_set: Optional[str] = None
    acct_secret_set: Optional[str] = None
    password_set: Optional[str] = None
    pkcs_passwd_set: Optional[str] = None
    priv_key_pwd_set: Optional[str] = None
    priv_key2_pwd_set: Optional[str] = None

    encryption: Encryption | str = Encryption.PSK2
    key: Optional[str] = None
    enabled: bool | str = True
    mode: WifiMode | str = WifiMode.ACCESSPOINT
    mesh_id: Optional[str] = None
    ssid: Optional[str] = None
    bssid: Optional[str] = None
    network: Optional[str] = "lan"
    mesh_fwding: Optional[str] = None
    mesh_rssi_threshold: Optional[str] = None
    hidden: Optional[str] = None
    isolate: bool | str = True
    bss_transition: Optional[str] = None
    ieee80211k: Optional[str] = None
    ieee80211w: Optional[str] = None
    disassoc_low_ack: Optional[str] = None
    trm_enabled: Optional[str] = None
    cipher: Cipher | str = Cipher.AUTO
    auth_server: Optional[str] = None
    auth_port: Optional[str] = None
    auth_secret: Optional[str] = None
    acct_server: Optional[str] = None
    acct_port: Optional[str] = None
    acct_secret: Optional[str] = None
    ieee80211r: Optional[str] = None
    nasid: Optional[str] = None
    mobility_domain: Optional[str] = None
    reassociation_deadline: Optional[str] = None
    ft_over_ds: Optional[str] = None
    eap_type: Optional[str] = None
    use_pkcs: Optional[str] = None
    pkcs_cert: Optional[str] = None
    pkcs_passwd: Optional[str] = None
    ca_cert: Optional[str] = None
    client_cert: Optional[str] = None
    priv_key: Optional[str] = None
    priv_key_pwd: Optional[str] = None
    auth: Optional[str] = None
    ca_cert2: Optional[str] = None
    client_cert2: Optional[str] = None
    priv_key2: Optional[str] = None
    priv_key2_pwd: Optional[str] = None
    identity: Optional[str] = None
    anonymous_identity: Optional[str] = None
    password: Optional[str] = None
    macfilter: Optional[str] = None
    maclist: List[str] = field(default_factory=list)
    delete_from_whitelist: Optional[str] = None
    short_preamble: Optional[str] = None
    dtim_period: Optional[str] = None
    wpa_group_rekey: Optional[str] = None
    skip_inactivity_poll: Optional[str] = None
    max_inactivity: Optional[str] = None
    max_listen_interval: Optional[str] = None
    device_files: Optional[str] = None
    device_files2: Optional[str] = None
    wds: Optional[str] = None
    wmm: Optional[str] = None
    scan_time: Optional[str] = None
    auto_reconnect: Optional[str] = None

    def asdict(self) -> dict:
        data = super().asdict()
        aliases = {
            "key_set": "key:set",
            "auth_secret_set": "auth_secret:set",
            "acct_secret_set": "acct_secret:set",
            "password_set": "password:set",
            "pkcs_passwd_set": "pkcs_passwd:set",
            "priv_key_pwd_set": "priv_key_pwd:set",
            "priv_key2_pwd_set": "priv_key2_pwd:set",
        }
        for source, target in aliases.items():
            data[target] = data.pop(source)

        return {k: v for k, v in data.items() if v is not None}

class WirelessInterfacesConfigResponse(BaseModel):
    id: str
    wifi_id: str
    network: str
    key: str
    ssid: str
    mode: WifiMode
    short_preamble: bool
    isolate: bool
    disassoc_low_ack: bool
    cipher: Cipher = Cipher.AUTO
    enabled: bool = True
    encryption: Encryption = Encryption.PSK2

class WirelessInterfacesDeleteResponse(BaseModel):
    # deleted interface
    id: str


class WirelessInterfacesStatusResponse(BaseModel):
    """Data model for wireless interfaces response."""

    class Client(BaseModel):
        """Data model for wireless client information."""
        expires: Optional[int] = None
        band: str
        ipaddr: Optional[str] = None
        hostname: Optional[str] = None
        tx_rate: int
        macaddr: str
        rx_rate: int
        signal: str
        interface: Optional[str] = None
        device: str

    id: str
    wifi_id: str
    ifname: str
    
    encryption: str
    # differs from docs says is required
    vht_supported: Optional[bool] = None
    num_assoc: int
    clients: List[Client] = Field(default_factory=list)
    status: str
    mode: Optional[str] = None
    multiple: Optional[bool] = None
    # ht_supported: bool
    ssid: str
    # conf_id: str
    # auth_status: int


class InterfacesEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self._client: "PonikaClient" = client

    def get_status(self, interface_id: int | str = None) -> List[WirelessInterfacesStatusResponse]:
        """Fetch wireless interfaces status from the device."""

        if interface_id:
            response = ApiResponse[WirelessInterfacesStatusResponse].model_validate(
                self._client._get(f"/wireless/interfaces/status/{interface_id}")
            )
        else:
            response = ApiResponse[list[WirelessInterfacesStatusResponse]].model_validate(
                self._client._get("/wireless/interfaces/status")
            )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data        

    
    def get_config(
        self,
        interface_id=None,
    ) -> List[WirelessInterfaceDefinition] | WirelessInterfaceDefinition:
        """Fetch wireless interfaces status from the device."""
        if interface_id:
            response = ApiResponse[WirelessInterfaceDefinition].model_validate(
                self._client._get(f"/wireless/interfaces/config/{interface_id}")
            )
        else:
            response = ApiResponse[list[WirelessInterfaceDefinition]].model_validate(
                self._client._get("/wireless/interfaces/config")
            )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data        


    def delete(self, interface_id) -> WirelessInterfacesDeleteResponse:
        response = self._client._delete(
            endpoint=f"/wireless/interfaces/config/{interface_id}",
            data_model=WirelessInterfacesDeleteResponse,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data        
    
    def create(self, interface: WirelessInterfaceDefinition) -> WirelessInterfacesConfigResponse:
        response = self._client._post_data(
            endpoint="/wireless/interfaces/config",
            params=interface,
            data_model=WirelessInterfacesConfigResponse,
        )

        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data
        
    
    def update(self, interface: WirelessInterfaceDefinition) -> WirelessInterfacesConfigResponse:
        interface_id = interface.id
        del interface.id

        response = self._client._put_data(
            endpoint=f"/wireless/interfaces/config/{interface_id}",
            params=interface,
            data_model=WirelessInterfacesConfigResponse,
        )
    
        if not response.success:
            raise TeltonikaApiException(response.errors)

        return response.data    
        
