"""Unit tests for network interfaces endpoint."""

import pytest
import responses

from ponika.config import PonikaConfig
from ponika.endpoints.interfaces.interfaces import (
    InterfaceAreaType,
    InterfaceCreatePayload,
    InterfaceMode,
    InterfaceUpdatePayload,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


INTERFACE_DATA = {
    'id': 'lan',
    'name': 'LAN',
    'area_type': 'lan',
    'enabled': '1',
    'proto': 'static',
    'mode': 'static',
    'ipaddr': '192.168.1.1',
    'netmask': '255.255.255.0',
    'ifname': ['eth0'],
    'password:set': '0',
}

INTERFACE_LIST_RESPONSE = {
    'success': True,
    'data': [INTERFACE_DATA],
}

INTERFACE_SINGLE_RESPONSE = {
    'success': True,
    'data': INTERFACE_DATA,
}

INTERFACE_STATUS_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'lan',
            'interface': 'lan',
            'ifname': 'br-lan',
            'proto': 'static',
            'up': True,
            'is_up': True,
            'rx_bytes': 100,
            'tx_bytes': 200,
            'ipaddrs': ['192.168.1.1/24'],
            'dns-server': [],
            'ipv4-address': [{'address': '192.168.1.1', 'mask': 24}],
            'subdevices': [
                {
                    'name': 'eth0',
                    'ifname': 'eth0',
                    'type': 'ethernet',
                    'is_up': True,
                }
            ],
        }
    ],
}


@pytest.mark.unit
@responses.activate
def test_interfaces_get_config_list(mock_client):
    mock_endpoint('get', '/interfaces/config', INTERFACE_LIST_RESPONSE)

    result = mock_client.interfaces.get_config()

    assert len(result) == 1
    assert result[0].id == 'lan'
    assert result[0].enabled is True
    assert result[0].area_type == InterfaceAreaType.LAN
    assert result[0].password_set is False


@pytest.mark.unit
@responses.activate
def test_interfaces_get_config_single(mock_client):
    mock_endpoint('get', '/interfaces/config/lan', INTERFACE_SINGLE_RESPONSE)

    result = mock_client.interfaces.get_config('lan')

    assert result.id == 'lan'
    assert result.ipaddr == '192.168.1.1'


@pytest.mark.unit
@responses.activate
def test_interfaces_create(mock_client):
    mock_endpoint('post', '/interfaces/config', INTERFACE_SINGLE_RESPONSE)

    payload = InterfaceCreatePayload(
        id='guest',
        area_type=InterfaceAreaType.LAN,
        name='Guest LAN',
        enabled=True,
        proto='static',
        mode=InterfaceMode.STATIC,
        ipaddr='192.168.50.1',
        netmask='255.255.255.0',
        ifname=['eth0.50'],
    )

    result = mock_client.interfaces.create(payload)

    assert result.id == 'lan'


@pytest.mark.unit
@responses.activate
def test_interfaces_update(mock_client):
    mock_endpoint('put', '/interfaces/config/lan', INTERFACE_SINGLE_RESPONSE)

    payload = InterfaceUpdatePayload(
        id='lan',
        name='LAN',
        enabled=True,
        metric='1',
    )

    result = mock_client.interfaces.update(payload)

    assert result.id == 'lan'


@pytest.mark.unit
@responses.activate
def test_interfaces_delete_accepts_empty_data(mock_client):
    mock_endpoint('delete', '/interfaces/config/guest', {'success': True})

    result = mock_client.interfaces.delete('guest')

    assert result.id == 'guest'


@pytest.mark.unit
@responses.activate
def test_interfaces_get_status_list(mock_client):
    mock_endpoint('get', '/interfaces/status', INTERFACE_STATUS_RESPONSE)

    result = mock_client.interfaces.get_status()

    assert len(result) == 1
    assert result[0].id == 'lan'
    assert result[0].dns_server == []
    assert result[0].ipv4_address[0].address == '192.168.1.1'


@pytest.mark.unit
@responses.activate
def test_interfaces_get_status_single(mock_client):
    mock_endpoint(
        'get',
        '/interfaces/status/lan',
        {'success': True, 'data': INTERFACE_STATUS_RESPONSE['data'][0]},
    )

    result = mock_client.interfaces.get_status('lan')

    assert result.id == 'lan'
    assert result.subdevices[0].ifname == 'eth0'


@pytest.mark.unit
@responses.activate
def test_interfaces_config_state_dry_run(mock_client):
    mock_endpoint('get', '/interfaces/config', INTERFACE_LIST_RESPONSE)

    desired = InterfaceCreatePayload(
        area_type=InterfaceAreaType.LAN,
        name='Guest LAN',
        enabled=True,
    )
    config = PonikaConfig(interfaces=[desired])

    result = mock_client.config.apply(
        config,
        dry_run=True,
        delete_unmanaged=False,
    )

    assert len(result.created) == 1
    assert result.created[0].section == 'interfaces'
    assert result.created[0].match_field == 'name'


@pytest.mark.unit
@responses.activate
def test_interfaces_error_raises(mock_client):
    mock_error_response(
        'get',
        '/interfaces/config',
        error_code=122,
        error_message='Not found',
        error_source='interfaces',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.interfaces.get_config()
