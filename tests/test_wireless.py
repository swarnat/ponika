"""Unit tests for wireless endpoints."""

import pytest
import responses
from pydantic import ValidationError

from ponika.endpoints.wireless.actions import (
    WirelessJoinPayload,
    WirelessScanPayload,
)
from ponika.endpoints.wireless.devices import WirelessDeviceUpdatePayload
from ponika.endpoints.wireless.interfaces import (
    WirelessInterfaceCreatePayload,
    WirelessInterfaceUpdatePayload,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


WIRELESS_DEVICES_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'radio0',
            'enabled': True,
            'hwmode': '11g',
            'channel': '6',
            'country': 'DE',
        }
    ],
}

WIRELESS_DEVICES_STATUS_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': 'radio0',
            'quality_max': 70,
            'disabled': False,
            'hardware_name': 'chip',
            'phyname': 'phy0',
            'mode': 'Master',
            'txpower_offset': 0,
            'type': 'mac80211',
            'hardware_id': {
                'device_id': 1,
                'subsystem_device_id': 1,
                'vendor_id': 1,
                'subsystem_vendor_id': 1,
            },
            'country': 'DE',
            'standard': '802.11n',
            'pending': False,
            'name': 'radio0',
            'autostart': True,
            'up': True,
            'noise': -95,
            'band': '2.4GHz',
            'macaddr': '00:11:22:33:44:55',
        }
    ],
}

WIRELESS_INTERFACES_LIST_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': '1',
            'ssid': 'TestWiFi',
            'mode': 'ap',
            'network': 'lan',
            'encryption': 'psk2',
            'enabled': '1',
            'isolate': '1',
            'cipher': 'auto',
            'maclist': [],
        }
    ],
}

WIRELESS_INTERFACES_STATUS_RESPONSE = {
    'success': True,
    'data': [
        {
            'id': '1',
            'wifi_id': 'radio0',
            'ifname': 'wlan0',
            'encryption': 'psk2',
            'num_assoc': 0,
            'clients': [],
            'status': 'up',
            'mode': 'Master',
            'multiple': False,
            'ssid': 'TestWiFi',
        }
    ],
}

WIRELESS_SCAN_RESPONSE = {
    'success': True,
    'data': [
        {
            'quality_max': 70,
            'ssid': 'Example WiFi',
            'encryption': {
                'enabled': True,
                'wpa': [2],
                'ciphers': ['ccmp'],
                'authentication': ['psk'],
            },
            'bssid': '00:11:22:33:44:55',
            'encryption_description': 'WPA2 PSK (CCMP)',
            'channel': 11,
            'ht_operation': {
                'secondary_channel_offset': 'no secondary',
                'channel_width': 20,
                'primary_channel': 11,
            },
            'mode': 'Master',
            'quality': 60,
            'signal': -50,
        }
    ],
}


@pytest.mark.unit
@responses.activate
def test_wireless_devices_get_config_list(mock_client):
    mock_endpoint(
        'get',
        '/wireless/devices/config',
        WIRELESS_DEVICES_LIST_RESPONSE,
    )

    result = mock_client.wireless.devices.get_config()

    assert len(result) == 1
    assert result[0].id == 'radio0'
    assert result[0].channel == '6'


@pytest.mark.unit
@responses.activate
def test_wireless_devices_update(mock_client):
    single = {
        'success': True,
        'data': WIRELESS_DEVICES_LIST_RESPONSE['data'][0],
    }
    mock_endpoint('put', '/wireless/devices/config/radio0', single)

    payload = WirelessDeviceUpdatePayload(
        id='radio0', enabled=True, channel='6'
    )
    result = mock_client.wireless.devices.update(payload)

    assert result.id == 'radio0'


@pytest.mark.unit
@responses.activate
def test_wireless_devices_status(mock_client):
    mock_endpoint(
        'get',
        '/wireless/devices/status',
        WIRELESS_DEVICES_STATUS_RESPONSE,
    )

    result = mock_client.wireless.devices.get_status()

    assert len(result) == 1
    assert result[0].id == 'radio0'
    assert result[0].up is True


@pytest.mark.unit
@responses.activate
def test_wireless_interfaces_get_config_list(mock_client):
    mock_endpoint(
        'get',
        '/wireless/interfaces/config',
        WIRELESS_INTERFACES_LIST_RESPONSE,
    )

    result = mock_client.wireless.interfaces.get_config()

    assert len(result) == 1
    assert result[0].ssid == 'TestWiFi'


@pytest.mark.unit
@responses.activate
def test_wireless_interfaces_create(mock_client):
    single = {
        'success': True,
        'data': WIRELESS_INTERFACES_LIST_RESPONSE['data'][0],
    }
    mock_endpoint('post', '/wireless/interfaces/config', single)

    payload = WirelessInterfaceCreatePayload(
        ssid='TestWiFi',
        mode='ap',
        encryption='psk2',
        key='12345678',
    )

    result = mock_client.wireless.interfaces.create(payload)

    assert result.ssid == 'TestWiFi'


@pytest.mark.unit
@responses.activate
def test_wireless_interfaces_update(mock_client):
    single = {
        'success': True,
        'data': WIRELESS_INTERFACES_LIST_RESPONSE['data'][0],
    }
    mock_endpoint('put', '/wireless/interfaces/config/1', single)

    payload = WirelessInterfaceUpdatePayload(id=1, ssid='TestWiFi')
    result = mock_client.wireless.interfaces.update(payload)

    assert result.ssid == 'TestWiFi'


@pytest.mark.unit
@responses.activate
def test_wireless_interfaces_delete(mock_client):
    delete_response = {'success': True, 'data': {'id': '1'}}
    mock_endpoint('delete', '/wireless/interfaces/config/1', delete_response)

    result = mock_client.wireless.interfaces.delete(1)

    assert result.id == '1'


@pytest.mark.unit
@responses.activate
def test_wireless_interfaces_status(mock_client):
    mock_endpoint(
        'get',
        '/wireless/interfaces/status',
        WIRELESS_INTERFACES_STATUS_RESPONSE,
    )

    result = mock_client.wireless.interfaces.get_status()

    assert len(result) == 1
    assert result[0].ifname == 'wlan0'


@pytest.mark.unit
@responses.activate
def test_wireless_devices_error_raises(mock_client):
    mock_error_response(
        'get',
        '/wireless/devices/config',
        error_code=122,
        error_message='Not found',
        error_source='wireless',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.wireless.devices.get_config()


@pytest.mark.unit
@responses.activate
def test_wireless_actions_scan(mock_client):
    mock_endpoint('post', '/wireless/actions/scan', WIRELESS_SCAN_RESPONSE)

    result = mock_client.wireless.actions.scan(
        WirelessScanPayload(device='radio0')
    )

    assert len(result) == 1
    assert result[0].ssid == 'Example WiFi'
    assert result[0].encryption is not None
    assert result[0].encryption.enabled is True
    assert (
        responses.calls[-1].request.body == b'{"data": {"device": "radio0"}}'
    )


@pytest.mark.unit
@responses.activate
def test_wireless_actions_join(mock_client):
    join_response = {
        'success': True,
        'data': WIRELESS_INTERFACES_LIST_RESPONSE['data'][0],
    }
    mock_endpoint('post', '/wireless/actions/join', join_response)

    result = mock_client.wireless.actions.join(
        WirelessJoinPayload(
            device='radio0',
            ssid='Example WiFi',
            password='secret-password',
        )
    )

    assert result.id == '1'
    assert result.ssid == 'TestWiFi'
    assert responses.calls[-1].request.body == (
        b'{"data": {"device": "radio0", "ssid": "Example WiFi", '
        b'"password": "secret-password"}}'
    )


def test_wireless_join_requires_ssid_or_bssid():
    with pytest.raises(ValidationError, match='either bssid or ssid'):
        WirelessJoinPayload(device='radio0')


@pytest.mark.unit
@responses.activate
@pytest.mark.parametrize('action', ['scan', 'join'])
def test_wireless_actions_error_raises(mock_client, action):
    mock_error_response(
        'post',
        f'/wireless/actions/{action}',
        error_code=422,
        error_message=f'Failed to {action}',
        error_source='wireless',
    )

    with pytest.raises(TeltonikaApiException):
        if action == 'scan':
            mock_client.wireless.actions.scan(WirelessScanPayload())
        else:
            mock_client.wireless.actions.join(
                WirelessJoinPayload(device='radio0', ssid='Example WiFi')
            )
