from typing import List, Optional

from ponika.endpoints import Endpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload


class WireguardPeerEntity:
    public_key: Optional[str] = None
    allowed_ips: Optional[List[str]] = None
    description: Optional[str] = None
    route_allowed_ips: Optional[bool] = None
    preshared_key: Optional[str] = None
    endpoint_host: Optional[str] = None
    endpoint_port: Optional[str] = None
    persistent_keepalive: Optional[str] = None
    table: Optional[str] = None
    tunlink: Optional[str] = None
    force_tunlink: Optional[bool] = None


class WireguardPeerConfigResponse(BaseModel, WireguardPeerEntity):
    id: str


class WireguardPeerDeleteResponse(BaseModel):
    id: str


class WireguardPeerGetPayload(BasePayload):
    id: str
    peers_id: Optional[str] = None
    all_options: Optional[bool] = None


class WireguardPeerCreatePayload(BasePayload, WireguardPeerEntity):
    id: str
    peer_id: Optional[str] = None


class WireguardPeerUpdatePayload(BasePayload, WireguardPeerEntity):
    id: str
    peers_id: str


class WireguardPeerBulkUpdatePayload(BasePayload, WireguardPeerEntity):
    id: str
    peers_id: str


class WireguardPeerDeletePayload(BasePayload):
    id: str
    peers_id: str


class WireguardPeerBulkDeletePayload(BasePayload):
    id: str
    peers_ids: List[str]


class PeersEndpoint(Endpoint):
    @staticmethod
    def _build_base_endpoint(interface_id: str) -> str:
        return f'/wireguard/{interface_id}/peers/config'

    @staticmethod
    def _peer_data_from_payload(payload: BasePayload) -> dict:
        data = payload.asdict()
        data.pop('id', None)

        peer_id = data.pop('peer_id', None)
        peers_id = data.pop('peers_id', None)
        if peer_id is not None:
            data['id'] = peer_id
        elif peers_id is not None:
            data['id'] = peers_id

        return data

    def get_config(
        self,
        payload: WireguardPeerGetPayload,
    ) -> List[WireguardPeerConfigResponse] | WireguardPeerConfigResponse:
        endpoint = self._build_base_endpoint(payload.id)
        if payload.peers_id:
            endpoint = f'{endpoint}/{payload.peers_id}'

        query_params = None
        if payload.all_options is not None:
            query_params = {'all_options': payload.all_options}

        response_model = (
            ApiResponse[WireguardPeerConfigResponse]
            if payload.peers_id
            else ApiResponse[List[WireguardPeerConfigResponse]]
        )
        response = response_model.model_validate(
            self._client._get(endpoint, params=query_params)
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def create(
        self,
        payload: WireguardPeerCreatePayload,
    ) -> WireguardPeerConfigResponse:
        response = self._client._post_data(
            endpoint=self._build_base_endpoint(payload.id),
            data_model=WireguardPeerConfigResponse,
            params=self._peer_data_from_payload(payload),
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def update(
        self,
        payload: WireguardPeerUpdatePayload,
    ) -> WireguardPeerConfigResponse:
        response = self._client._put_data(
            endpoint=f'{self._build_base_endpoint(payload.id)}/{payload.peers_id}',
            data_model=WireguardPeerConfigResponse,
            params=self._peer_data_from_payload(payload),
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def update_bulk(
        self,
        payloads: List[WireguardPeerBulkUpdatePayload],
    ) -> List[WireguardPeerConfigResponse]:
        if not payloads:
            raise ValueError('payloads must not be empty')

        interface_id = payloads[0].id
        if any(item.id != interface_id for item in payloads):
            raise ValueError('all payloads must use the same id')

        data = [self._peer_data_from_payload(payload) for payload in payloads]
        response = self._client._put(
            endpoint=self._build_base_endpoint(interface_id),
            data_model=object,
            params={'data': data},
        )

        response_obj = ApiResponse[
            List[WireguardPeerConfigResponse]
        ].model_validate(response.model_dump(mode='python'))
        if not response_obj.success or response_obj.data is None:
            raise TeltonikaApiException(response_obj.errors)

        return response_obj.data

    def delete(
        self,
        payload: WireguardPeerDeletePayload,
    ) -> WireguardPeerDeleteResponse:
        response = self._client._delete(
            endpoint=f'{self._build_base_endpoint(payload.id)}/{payload.peers_id}',
            data_model=WireguardPeerDeleteResponse,
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def delete_bulk(
        self,
        payload: WireguardPeerBulkDeletePayload,
    ) -> List[WireguardPeerDeleteResponse]:
        response = self._client._delete(
            endpoint=self._build_base_endpoint(payload.id),
            data_model=object,
            params={'data': payload.peers_ids},
        )

        response_obj = ApiResponse[
            List[WireguardPeerDeleteResponse]
        ].model_validate(response.model_dump(mode='python'))
        if not response_obj.success or response_obj.data is None:
            raise TeltonikaApiException(response_obj.errors)

        return response_obj.data
