from typing import List

from ponika.endpoints import DynamicPathCRUDEndpoint, Endpoint
from ponika.models import BaseModel, BasePayload


class OpenvpnTlsClientBase:
    name: str | None = None
    local_ip: str | None = None
    remote_ip: str | None = None
    local_net: str | None = None
    private_network_ipv6: str | None = None
    local_ipv6: str | None = None
    private_network: str | None = None
    covered_network: List[str] | None = None


class OpenvpnTlsClientRequiredFields:
    common_name: str


class OpenvpnTlsClientOptionalRequiredFields:
    common_name: str | None = None


class OpenvpnTlsClientResponse(
    BaseModel,
    OpenvpnTlsClientRequiredFields,
    OpenvpnTlsClientBase,
):
    id: str | None = None


class OpenvpnTlsClientCreatePayload(
    BasePayload,
    OpenvpnTlsClientRequiredFields,
    OpenvpnTlsClientBase,
):
    id: str | None = None


class OpenvpnTlsClientUpdatePayload(
    BasePayload,
    OpenvpnTlsClientOptionalRequiredFields,
    OpenvpnTlsClientBase,
):
    id: str


class OpenvpnTlsClientDeleteResponse(BaseModel):
    id: str


class OpenvpnTlsClientConfigEndpoint(
    DynamicPathCRUDEndpoint[
        OpenvpnTlsClientCreatePayload,
        OpenvpnTlsClientResponse,
        OpenvpnTlsClientUpdatePayload,
        OpenvpnTlsClientDeleteResponse,
    ]
):
    endpoint_path_template = '/openvpn/{openvpn_id}/clients/config'

    config_response_model = OpenvpnTlsClientResponse
    create_model = OpenvpnTlsClientCreatePayload
    update_model = OpenvpnTlsClientUpdatePayload
    delete_reponse_model = OpenvpnTlsClientDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True


class TlsClientsEndpoint(Endpoint):
    def config(self, openvpn_id: str | int) -> OpenvpnTlsClientConfigEndpoint:
        return OpenvpnTlsClientConfigEndpoint(
            self._client,
            openvpn_id=openvpn_id,
        )
