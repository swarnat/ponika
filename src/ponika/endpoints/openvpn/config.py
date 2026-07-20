from typing import List

from pydantic import Field, model_validator

from ponika.endpoints import CRUDEndpoint, StatusEndpoint
from ponika.endpoints.openvpn.enums import (
    OpenvpnAuth,
    OpenvpnAuthMode,
    OpenvpnCipher,
    OpenvpnCompression,
    OpenvpnConfigParsed,
    OpenvpnConfiguration,
    OpenvpnDevice,
    OpenvpnDh,
    OpenvpnExternalService,
    OpenvpnProtocol,
    OpenvpnServerList,
    OpenvpnTlsCipher,
    OpenvpnTlsCipherList,
    OpenvpnTlsSecurity,
    OpenvpnTopology,
    OpenvpnType,
)
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel, BasePayload


class OpenvpnConfigBase:
    enable: bool | None = None
    configuration: OpenvpnConfiguration | None = None
    auth_mode: OpenvpnAuthMode | None = None
    topology: OpenvpnTopology | None = None
    proto: OpenvpnProtocol | None = None
    port: str | None = None
    push: List[str] | None = None
    extra: List[str] | None = None
    remote: List[str] | None = None
    to_bridge: str | None = None
    server_ip: str | None = None
    server_netmask: str | None = None
    network: List[str] | None = None
    ifconfig_pool_start: str | None = None
    ifconfig_pool_end: str | None = None
    server_ipv6: str | None = None
    ifconfig_ipv6_pool: str | None = None
    comp_lzo: OpenvpnCompression | None = None
    client_to_client: bool | None = None
    resolv_retry: str | None = None
    keepalive: str | None = None
    user: str | None = None
    password: str | None = Field(default=None, alias='pass')
    userpass: str | None = None
    cipher: OpenvpnCipher | None = None
    data_ciphers: List[str] | None = None
    duplicate_cn: bool | None = None
    auth: OpenvpnAuth | None = None
    tls_security: OpenvpnTlsSecurity | None = None
    key_direction: bool | None = None
    use_pkcs: bool | None = None
    device_files: str | None = None
    tls_auth: str | None = None
    tls_crypt: str | None = None
    pkcs12: str | None = None
    ca: str | None = None
    cert: str | None = None
    key: str | None = None
    dh: OpenvpnDh | None = None
    crl_verify: str | None = None
    askpass: str | None = None
    secret: str | None = None
    parse: bool | None = None
    config_parsed: OpenvpnConfigParsed | None = None
    config: str | None = None
    external_service: OpenvpnExternalService | None = None
    server_list: OpenvpnServerList | None = None
    local_ip: str | None = None
    remote_ip: str | None = None
    local_ipv6: str | None = None
    remote_ipv6: str | None = None
    enable_external: bool | None = None
    upload_files: bool | None = None
    tls_cipher_list: OpenvpnTlsCipherList | None = None
    enable_custom: bool | None = None
    tls_cipher: List[OpenvpnTlsCipher] | None = None
    cipher_custom: List[str] | None = None
    network_ip: str | None = None
    network_mask: str | None = None
    route_ipv6: str | None = None
    decrypt: str | None = None


class OpenvpnConfigRequiredFields:
    type: OpenvpnType
    name: str
    dev: OpenvpnDevice


class OpenvpnConfigOptionalRequiredFields:
    type: OpenvpnType | None = None
    name: str | None = None
    dev: OpenvpnDevice | None = None


class OpenvpnConfigResponse(
    BaseModel,
    OpenvpnConfigOptionalRequiredFields,
    OpenvpnConfigBase,
):
    id: str | None = None

    @model_validator(mode='before')
    @classmethod
    def use_id_as_missing_name(cls, data):
        if (
            isinstance(data, dict)
            and data.get('name') is None
            and data.get('id')
        ):
            return {**data, 'name': data['id']}
        return data


class OpenvpnConfigCreatePayload(
    BasePayload,
    OpenvpnConfigRequiredFields,
    OpenvpnConfigBase,
):
    pass


class OpenvpnConfigUpdatePayload(
    BasePayload,
    OpenvpnConfigOptionalRequiredFields,
    OpenvpnConfigBase,
):
    id: str


class OpenvpnConfigDeleteResponse(BaseModel):
    id: str


class OpenvpnConfigUploadResponse(BaseModel):
    path: str


class OpenvpnConfigCreateWithUploadResponse(BaseModel):
    created: OpenvpnConfigResponse
    upload: OpenvpnConfigUploadResponse
    config: OpenvpnConfigResponse


class OpenvpnStatusClient(BaseModel):
    uptime: str | None = None
    vpn_ip: str | None = None
    last_ref: str | None = None
    name: str | None = None
    tx: str | None = None
    rx: str | None = None
    ip: str | None = None
    vpn_ip6: str | None = None
    mac: str | None = None


class OpenvpnStatusResponse(BaseModel):
    type: OpenvpnType | None = None
    protocol: OpenvpnDevice | None = None
    updated: str | None = None
    rx: str | None = None
    tx: str | None = None
    status: str | None = None
    uptime: str | None = None
    clients_connected: str | None = None
    clients: List[OpenvpnStatusClient] | None = None
    clients_all: str | None = None
    ipaddress_remote: str | None = None
    ipaddress: str | None = None
    server: str | None = None
    logs: str | None = None
    name: str | None = None
    device: str | None = None


class ConfigEndpoint(
    CRUDEndpoint[
        OpenvpnConfigCreatePayload,
        OpenvpnConfigResponse,
        OpenvpnConfigUpdatePayload,
        OpenvpnConfigDeleteResponse,
    ],
    StatusEndpoint[OpenvpnStatusResponse],
):
    endpoint_path = '/openvpn/config'
    status_endpoint_path = '/openvpn/status'

    config_response_model = OpenvpnConfigResponse
    status_response_model = OpenvpnStatusResponse
    create_model = OpenvpnConfigCreatePayload
    update_model = OpenvpnConfigUpdatePayload
    delete_reponse_model = OpenvpnConfigDeleteResponse

    allow_bulk_update = True
    bulk_update_strip_item_id = False
    allow_bulk_delete = True

    def create(
        self,
        payload: OpenvpnConfigCreatePayload,
    ) -> OpenvpnConfigResponse:
        data = payload.asdict()
        # RutOS uses the user-facing name as its section ID, but accepts it
        # only under `id`. Sending `name` produces error 103 (Invalid option).
        data['id'] = data.pop('name')
        # Despite being present in the shared OpenAPI schema, `configuration`
        # is rejected on create. Custom mode is selected by uploading `config`.
        data.pop('configuration', None)

        response = self._client._post_data(
            endpoint=self.endpoint_path,
            params=data,
            data_model=self.config_response_model,
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)
        return response.data

    def create_with_config_upload(
        self,
        payload: OpenvpnConfigCreatePayload,
        file_path: str,
    ) -> OpenvpnConfigCreateWithUploadResponse:
        if payload.configuration != OpenvpnConfiguration.CUSTOM:
            raise ValueError(
                'create_with_config_upload requires '
                'configuration=OpenvpnConfiguration.CUSTOM.'
            )

        created = self.create(payload)
        upload = self.upload_config(payload.name, file_path)
        config = self.update(
            OpenvpnConfigUpdatePayload(
                id=payload.name,
                config=upload.path,
            )
        )
        return OpenvpnConfigCreateWithUploadResponse(
            created=created,
            upload=upload,
            config=config,
        )

    def upload_config(
        self,
        item_id: str | int,
        file_path: str,
    ) -> OpenvpnConfigUploadResponse:
        response = self._client._post_files(
            endpoint=f'{self.endpoint_path}/{item_id}',
            data_model=OpenvpnConfigUploadResponse,
            files={'file': file_path},
            params={'option': 'config'},
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def download_config(self, item_id: str | int) -> bytes:
        response = self._client._post_raw(
            endpoint=f'/openvpn/{item_id}/actions/download'
        )
        response.raise_for_status()
        return response.content
