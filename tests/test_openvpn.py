"""Unit tests for OpenVPN endpoints."""

import json

import pytest
import responses

from ponika.endpoints.openvpn.config import (
    OpenvpnConfigCreatePayload,
    OpenvpnConfigUpdatePayload,
)
from ponika.endpoints.openvpn.enums import (
    OpenvpnConfiguration,
    OpenvpnDevice,
    OpenvpnType,
)
from ponika.endpoints.openvpn.tls_clients import (
    OpenvpnTlsClientCreatePayload,
    OpenvpnTlsClientUpdatePayload,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import (
    BASE_URL,
    LOGIN_RESPONSE,
    mock_endpoint,
    mock_error_response,
)


def _request_json_body(call_index: int) -> dict:
    body = responses.calls[call_index].request.body
    if body is None:
        return {}
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return json.loads(body)


OPENVPN_CONFIG_ITEM = {
    'id': 'vpn0',
    'enable': '1',
    'type': 'client',
    'name': 'office-vpn',
    'configuration': 'custom',
    'dev': 'tun',
    'proto': 'udp',
    'port': '1194',
    'parse': '1',
}

OPENVPN_CONFIG_SINGLE_RESPONSE = {
    'success': True,
    'data': OPENVPN_CONFIG_ITEM,
}

OPENVPN_CONFIG_LIST_RESPONSE = {
    'success': True,
    'data': [OPENVPN_CONFIG_ITEM],
}

OPENVPN_DELETE_RESPONSE = {
    'success': True,
    'data': {'id': 'vpn0'},
}

OPENVPN_STATUS_RESPONSE = {
    'success': True,
    'data': [
        {
            'type': 'client',
            'protocol': 'tun',
            'status': '1',
            'name': 'office-vpn',
            'rx': '100',
            'tx': '200',
        }
    ],
}

OPENVPN_TLS_CLIENT_ITEM = {
    'id': 'client1',
    'name': 'Laptop',
    'common_name': 'laptop.example',
    'local_ip': '172.16.1.6',
    'remote_ip': '172.16.1.5',
    'covered_network': ['192.168.10.0/24'],
}

OPENVPN_TLS_CLIENT_SINGLE_RESPONSE = {
    'success': True,
    'data': OPENVPN_TLS_CLIENT_ITEM,
}

OPENVPN_TLS_CLIENT_LIST_RESPONSE = {
    'success': True,
    'data': [OPENVPN_TLS_CLIENT_ITEM],
}


@pytest.mark.unit
@responses.activate
def test_openvpn_config_get_list(mock_client):
    mock_endpoint('get', '/openvpn/config', OPENVPN_CONFIG_LIST_RESPONSE)

    result = mock_client.openvpn.config.get_config()

    assert len(result) == 1
    assert result[0].id == 'vpn0'
    assert result[0].enable is True


@pytest.mark.unit
@responses.activate
def test_openvpn_config_get_list_accepts_web_ui_entry_without_name(
    mock_client,
):
    web_ui_config = {
        key: value
        for key, value in OPENVPN_CONFIG_ITEM.items()
        if key != 'name'
    }
    mock_endpoint(
        'get',
        '/openvpn/config',
        {'success': True, 'data': [web_ui_config]},
    )

    result = mock_client.openvpn.config.get_config()

    assert len(result) == 1
    assert result[0].id == 'vpn0'
    assert result[0].name == 'vpn0'
    assert result[0].type == OpenvpnType.CLIENT
    assert result[0].dev == OpenvpnDevice.TUN


@pytest.mark.unit
@responses.activate
def test_openvpn_config_create(mock_client):
    mock_endpoint('post', '/openvpn/config', OPENVPN_CONFIG_SINGLE_RESPONSE)

    payload = OpenvpnConfigCreatePayload(
        enable=True,
        type=OpenvpnType.CLIENT,
        name='office-vpn',
        dev=OpenvpnDevice.TUN,
        configuration=OpenvpnConfiguration.CUSTOM,
        parse=True,
    )
    result = mock_client.openvpn.config.create(payload)

    assert result.id == 'vpn0'
    request_body = _request_json_body(1)
    assert request_body['data']['enable'] == '1'
    assert request_body['data']['type'] == 'client'
    assert request_body['data']['parse'] == '1'
    assert request_body['data']['id'] == 'office-vpn'
    assert 'name' not in request_body['data']
    assert 'configuration' not in request_body['data']


@pytest.mark.unit
@responses.activate
def test_openvpn_config_update(mock_client):
    mock_endpoint(
        'put', '/openvpn/config/vpn0', OPENVPN_CONFIG_SINGLE_RESPONSE
    )

    payload = OpenvpnConfigUpdatePayload(
        id='vpn0',
        enable=False,
        name='office-vpn',
    )
    result = mock_client.openvpn.config.update(payload)

    assert result.id == 'vpn0'
    request_body = _request_json_body(1)
    assert request_body['data']['enable'] == '0'
    assert 'id' not in request_body['data']


@pytest.mark.unit
@responses.activate
def test_openvpn_config_delete(mock_client):
    mock_endpoint('delete', '/openvpn/config/vpn0', OPENVPN_DELETE_RESPONSE)

    result = mock_client.openvpn.config.delete('vpn0')

    assert result.id == 'vpn0'


@pytest.mark.unit
@responses.activate
def test_openvpn_config_status(mock_client):
    mock_endpoint('get', '/openvpn/status', OPENVPN_STATUS_RESPONSE)

    result = mock_client.openvpn.config.get_status()

    assert len(result) == 1
    assert result[0].name == 'office-vpn'
    assert result[0].protocol == OpenvpnDevice.TUN


@pytest.mark.unit
@responses.activate
def test_openvpn_upload_config(mock_client, tmp_path):
    config_file = tmp_path / 'client.ovpn'
    config_file.write_text('client\ndev tun\n')

    responses.post(f'{BASE_URL}/login', json=LOGIN_RESPONSE, status=200)
    responses.post(
        f'{BASE_URL}/openvpn/config/vpn0',
        json={'success': True, 'data': {'path': '/etc/openvpn/client.ovpn'}},
        status=200,
    )

    result = mock_client.openvpn.config.upload_config('vpn0', str(config_file))

    assert result.path == '/etc/openvpn/client.ovpn'
    request = responses.calls[1].request
    body = request.body.decode('utf-8')
    assert 'name="option"' in body
    assert 'config' in body
    assert 'name="file"' in body
    assert 'client.ovpn' in body


@pytest.mark.unit
@responses.activate
def test_openvpn_create_with_config_upload(mock_client, tmp_path):
    config_file = tmp_path / 'client.ovpn'
    config_file.write_text('client\ndev tun\n')
    mock_endpoint('post', '/openvpn/config', OPENVPN_CONFIG_SINGLE_RESPONSE)
    responses.post(
        f'{BASE_URL}/openvpn/config/office-vpn',
        json={'success': True, 'data': {'path': '/etc/openvpn/client.ovpn'}},
        status=200,
    )
    updated_item = {
        **OPENVPN_CONFIG_ITEM,
        'id': 'office-vpn',
        'name': 'office-vpn',
        'config': '/etc/openvpn/client.ovpn',
    }
    responses.put(
        f'{BASE_URL}/openvpn/config/office-vpn',
        json={'success': True, 'data': updated_item},
        status=200,
    )
    payload = OpenvpnConfigCreatePayload(
        enable=False,
        type=OpenvpnType.CLIENT,
        name='office-vpn',
        dev=OpenvpnDevice.TUN,
        configuration=OpenvpnConfiguration.CUSTOM,
    )

    result = mock_client.openvpn.config.create_with_config_upload(
        payload,
        str(config_file),
    )

    assert result.created.id == 'vpn0'
    assert result.upload.path == '/etc/openvpn/client.ovpn'
    assert result.config.id == 'office-vpn'
    assert result.config.config == '/etc/openvpn/client.ovpn'
    assert responses.calls[1].request.url.endswith('/openvpn/config')
    assert responses.calls[2].request.url.endswith(
        '/openvpn/config/office-vpn'
    )
    assert responses.calls[3].request.url.endswith(
        '/openvpn/config/office-vpn'
    )
    assert responses.calls[3].request.method == 'PUT'
    create_body = _request_json_body(1)
    assert create_body['data']['id'] == 'office-vpn'
    assert 'configuration' not in create_body['data']
    update_body = _request_json_body(3)
    assert update_body['data'] == {'config': '/etc/openvpn/client.ovpn'}


@pytest.mark.unit
def test_openvpn_create_with_config_upload_requires_custom(mock_client):
    payload = OpenvpnConfigCreatePayload(
        enable=False,
        type=OpenvpnType.CLIENT,
        name='office-vpn',
        dev=OpenvpnDevice.TUN,
        configuration=OpenvpnConfiguration.MANUAL,
    )

    with pytest.raises(ValueError, match='OpenvpnConfiguration.CUSTOM'):
        mock_client.openvpn.config.create_with_config_upload(
            payload,
            '/path/to/client.ovpn',
        )


@pytest.mark.unit
@responses.activate
def test_openvpn_download_config(mock_client):
    responses.post(f'{BASE_URL}/login', json=LOGIN_RESPONSE, status=200)
    responses.post(
        f'{BASE_URL}/openvpn/vpn0/actions/download',
        body=b'client\ndev tun\n',
        status=200,
    )

    result = mock_client.openvpn.config.download_config('vpn0')

    assert result == b'client\ndev tun\n'


@pytest.mark.unit
@responses.activate
def test_openvpn_tls_clients_get_and_create(mock_client):
    mock_endpoint(
        'get',
        '/openvpn/vpn0/clients/config',
        OPENVPN_TLS_CLIENT_LIST_RESPONSE,
    )
    mock_endpoint(
        'post',
        '/openvpn/vpn0/clients/config',
        OPENVPN_TLS_CLIENT_SINGLE_RESPONSE,
        include_login=False,
    )
    endpoint = mock_client.openvpn.tls_clients.config('vpn0')

    clients = endpoint.get_config()
    created = endpoint.create(
        OpenvpnTlsClientCreatePayload(
            id='client1',
            name='Laptop',
            common_name='laptop.example',
        )
    )

    assert clients[0].common_name == 'laptop.example'
    assert created.id == 'client1'
    request_body = _request_json_body(2)
    assert request_body['data']['common_name'] == 'laptop.example'


@pytest.mark.unit
@responses.activate
def test_openvpn_tls_clients_update_and_delete(mock_client):
    mock_endpoint(
        'put',
        '/openvpn/vpn0/clients/config/client1',
        OPENVPN_TLS_CLIENT_SINGLE_RESPONSE,
    )
    mock_endpoint(
        'delete',
        '/openvpn/vpn0/clients/config/client1',
        {'success': True, 'data': {'id': 'client1'}},
        include_login=False,
    )
    endpoint = mock_client.openvpn.tls_clients.config('vpn0')

    updated = endpoint.update(
        OpenvpnTlsClientUpdatePayload(
            id='client1',
            local_ip='172.16.1.6',
        )
    )
    deleted = endpoint.delete('client1')

    assert updated.id == 'client1'
    assert deleted.id == 'client1'


@pytest.mark.unit
@responses.activate
def test_openvpn_config_error_raises(mock_client):
    mock_error_response(
        'get',
        '/openvpn/config',
        error_code=122,
        error_message='Not found',
        error_source='openvpn',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.openvpn.config.get_config()


@pytest.mark.unit
@responses.activate
def test_openvpn_create_error_without_source_raises_api_exception(mock_client):
    mock_endpoint(
        'post',
        '/openvpn/config',
        {
            'success': False,
            'errors': [
                {
                    'code': 113,
                    'error': "'mugler' is not a valid string format allowed.",
                }
            ],
        },
    )
    payload = OpenvpnConfigCreatePayload(
        enable=False,
        type=OpenvpnType.CLIENT,
        name='mugler',
        dev=OpenvpnDevice.TUN,
    )

    with pytest.raises(TeltonikaApiException) as exc_info:
        mock_client.openvpn.config.create(payload)

    api_errors = exc_info.value.args[0]
    assert api_errors[0].code == 113
    assert api_errors[0].source is None
    assert str(api_errors[0]) == (
        "Error 113: 'mugler' is not a valid string format allowed."
    )
