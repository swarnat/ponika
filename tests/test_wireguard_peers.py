"""Unit tests for wireguard peers endpoints."""

import json

import pytest
import responses

from ponika.endpoints.wireguard.peers import (
    WireguardPeerBulkDeletePayload,
    WireguardPeerBulkUpdatePayload,
    WireguardPeerCreatePayload,
    WireguardPeerDeletePayload,
    WireguardPeerGetPayload,
    WireguardPeerUpdatePayload,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


def _request_json_body(call_index: int) -> dict:
    body = responses.calls[call_index].request.body
    if body is None:
        return {}
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return json.loads(body)


WIREGUARD_PEERS_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'peer1',
            'public_key': 'p' * 44,
            'allowed_ips': ['10.10.0.2/32'],
            'route_allowed_ips': '1',
            'endpoint_host': 'example.org',
            'endpoint_port': '51820',
        }
    ],
}

WIREGUARD_PEER_SINGLE_RESPONSE = {
    'success': True,
    'data': WIREGUARD_PEERS_LIST_RESPONSE['data'][0],
}

WIREGUARD_PEER_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': 'peer1'},
}

WIREGUARD_PEER_BULK_DELETE_RESPONSE = {
    'success': True,
    'data': [{'id': 'peer1'}, {'id': 'peer2'}],
}


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_get_list(mock_client):
    mock_endpoint(
        'get',
        '/wireguard/wg0/peers/config',
        WIREGUARD_PEERS_LIST_RESPONSE,
    )

    result = mock_client.wireguard.peers.get_config(
        WireguardPeerGetPayload(id='wg0')
    )

    assert len(result) == 1
    assert result[0].id == 'peer1'
    assert result[0].route_allowed_ips is True


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_get_single(mock_client):
    mock_endpoint(
        'get',
        '/wireguard/wg0/peers/config/peer1',
        WIREGUARD_PEER_SINGLE_RESPONSE,
    )

    result = mock_client.wireguard.peers.get_config(
        WireguardPeerGetPayload(id='wg0', peers_id='peer1')
    )

    assert result.id == 'peer1'


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_create(mock_client):
    mock_endpoint(
        'post',
        '/wireguard/wg0/peers/config',
        WIREGUARD_PEER_SINGLE_RESPONSE,
    )

    result = mock_client.wireguard.peers.create(
        WireguardPeerCreatePayload(
            id='wg0',
            peer_id='peer1',
            public_key='p' * 44,
            allowed_ips=['10.10.0.2/32'],
            route_allowed_ips=True,
        )
    )

    assert result.id == 'peer1'
    request_body = _request_json_body(1)
    assert request_body['data']['id'] == 'peer1'
    assert request_body['data']['route_allowed_ips'] == '1'


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_update(mock_client):
    mock_endpoint(
        'put',
        '/wireguard/wg0/peers/config/peer1',
        WIREGUARD_PEER_SINGLE_RESPONSE,
    )

    result = mock_client.wireguard.peers.update(
        WireguardPeerUpdatePayload(
            id='wg0',
            peers_id='peer1',
            public_key='p' * 44,
            allowed_ips=['10.10.0.3/32'],
            route_allowed_ips=False,
        )
    )

    assert result.id == 'peer1'
    request_body = _request_json_body(1)
    assert request_body['data']['id'] == 'peer1'
    assert request_body['data']['route_allowed_ips'] == '0'


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_update_bulk(mock_client):
    bulk_response = {
        'success': True,
        'data': [
            WIREGUARD_PEERS_LIST_RESPONSE['data'][0],
            {
                **WIREGUARD_PEERS_LIST_RESPONSE['data'][0],
                'id': 'peer2',
                'route_allowed_ips': '0',
            },
        ],
    }
    mock_endpoint('put', '/wireguard/wg0/peers/config', bulk_response)

    result = mock_client.wireguard.peers.update_bulk(
        [
            WireguardPeerBulkUpdatePayload(
                id='wg0',
                peers_id='peer1',
                public_key='p' * 44,
                allowed_ips=['10.10.0.2/32'],
            ),
            WireguardPeerBulkUpdatePayload(
                id='wg0',
                peers_id='peer2',
                public_key='q' * 44,
                allowed_ips=['10.10.0.4/32'],
            ),
        ]
    )

    assert len(result) == 2
    assert result[1].id == 'peer2'
    request_body = _request_json_body(1)
    assert request_body['data'][0]['id'] == 'peer1'
    assert request_body['data'][1]['id'] == 'peer2'


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_delete(mock_client):
    mock_endpoint(
        'delete',
        '/wireguard/wg0/peers/config/peer1',
        WIREGUARD_PEER_DELETE_RESPONSE,
    )

    result = mock_client.wireguard.peers.delete(
        WireguardPeerDeletePayload(id='wg0', peers_id='peer1')
    )

    assert result.id == 'peer1'


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_delete_bulk(mock_client):
    mock_endpoint(
        'delete',
        '/wireguard/wg0/peers/config',
        WIREGUARD_PEER_BULK_DELETE_RESPONSE,
    )

    result = mock_client.wireguard.peers.delete_bulk(
        WireguardPeerBulkDeletePayload(
            id='wg0',
            peers_ids=['peer1', 'peer2'],
        )
    )

    assert result[0].id == 'peer1'
    assert result[1].id == 'peer2'
    request_body = _request_json_body(1)
    assert request_body['data'] == ['peer1', 'peer2']


@pytest.mark.unit
@responses.activate
def test_wireguard_peers_error_raises(mock_client):
    mock_error_response(
        'get',
        '/wireguard/wg0/peers/config',
        error_code=122,
        error_message='Not found',
        error_source='wireguard',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.wireguard.peers.get_config(
            WireguardPeerGetPayload(id='wg0')
        )
