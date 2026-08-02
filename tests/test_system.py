"""Unit tests for all System API operations."""

import json

import pytest
import responses
from pydantic import ValidationError

from ponika.endpoints.system.actions import ChangePasswordFirstLoginPayload
from ponika.endpoints.system.banner import BannerUpdatePayload
from ponika.endpoints.system.buttons import ButtonUpdatePayload
from ponika.endpoints.system.enums import ButtonHandler, DeviceParameterType
from ponika.endpoints.system.general import GeneralUpdatePayload
from ponika.endpoints.system.led import LedUpdatePayload
from tests.mocks import mock_endpoint


def _body(index: int) -> dict:
    body = responses.calls[index].request.body
    if isinstance(body, bytes):
        body = body.decode()
    return json.loads(body or '{}')


@pytest.mark.unit
@responses.activate
def test_system_actions(mock_client):
    mock_endpoint('post', '/system/actions/reboot', {'success': True})
    mock_endpoint(
        'post',
        '/system/actions/change_password_firstlogin',
        {'success': True},
        include_login=False,
    )

    mock_client.system.actions.reboot()
    mock_client.system.actions.change_password_first_login(
        ChangePasswordFirstLoginPayload(
            password='Secure-password-1',
            password_confirm='Secure-password-1',
        )
    )

    assert _body(2) == {
        'data': {
            'password': 'Secure-password-1',
            'password_confirm': 'Secure-password-1',
        }
    }


def test_change_password_rejects_mismatch():
    with pytest.raises(ValidationError, match='must match'):
        ChangePasswordFirstLoginPayload(
            password='SecurePassword1', password_confirm='OtherPassword1'
        )


@pytest.mark.parametrize(
    ('password', 'message'),
    [
        ('Short1', 'at least 8 characters'),
        ('PASSWORD1', 'lowercase character'),
        ('password1', 'uppercase character'),
        ('Password', 'number'),
    ],
)
def test_change_password_rejects_insufficient_complexity(password, message):
    with pytest.raises(ValidationError, match=message):
        ChangePasswordFirstLoginPayload(
            password=password,
            password_confirm=password,
        )


@pytest.mark.unit
@responses.activate
@pytest.mark.parametrize(
    ('attribute', 'path', 'payload', 'response_data'),
    [
        (
            'banner',
            '/system/banner/config',
            BannerUpdatePayload(
                id='login', enabled=True, title='Welcome', message='Authorized'
            ),
            {
                'id': 'login',
                'enabled': '1',
                'title': 'Welcome',
                'message': 'Authorized',
            },
        ),
        (
            'buttons',
            '/system/buttons/config',
            ButtonUpdatePayload(id='reset', min='3', max='8', enabled=True),
            {
                'id': 'reset',
                'min': '3',
                'max': '8',
                'enabled': '1',
                'action': 'hold',
                'handler': 'reboot',
            },
        ),
        (
            'general',
            '/system/config',
            GeneralUpdatePayload(
                id='general', hostname='router', data_analytics=False
            ),
            {
                'id': 'general',
                'hostname': 'router',
                'data_analytics': '0',
                'firstlogin': '0',
            },
        ),
        (
            'led',
            '/system/led/config',
            LedUpdatePayload(id='all', enabled=False),
            {'id': 'all', 'enabled': '0'},
        ),
    ],
)
def test_system_configuration_get_single_update_and_bulk(
    mock_client, attribute, path, payload, response_data
):
    endpoint = getattr(mock_client.system, attribute)
    mock_endpoint('get', path, {'success': True, 'data': [response_data]})
    mock_endpoint(
        'get',
        f'{path}/{payload.id}',
        {'success': True, 'data': response_data},
        include_login=False,
    )
    mock_endpoint(
        'put',
        f'{path}/{payload.id}',
        {'success': True, 'data': response_data},
        include_login=False,
    )
    mock_endpoint(
        'put',
        path,
        {'success': True, 'data': [response_data]},
        include_login=False,
    )

    all_items = endpoint.get_config()
    single = endpoint.get_config(payload.id)
    updated = endpoint.update(payload)
    bulk = endpoint.update_bulk([payload])

    assert all_items[0].id == payload.id
    assert single.id == payload.id
    assert updated.id == payload.id
    assert bulk[0].id == payload.id
    assert 'id' not in _body(3)['data']
    assert _body(4)['data'][0]['id'] == payload.id
    if hasattr(updated, 'enabled'):
        assert _body(3)['data'].get('enabled') in ('0', '1', None)
    if attribute == 'buttons':
        assert single.handler == ButtonHandler.REBOOT


def test_button_press_time_validation():
    with pytest.raises(ValidationError, match='between 0 and 60'):
        ButtonUpdatePayload(id='reset', min='99')


@pytest.mark.unit
@responses.activate
def test_system_general_languages(mock_client):
    mock_endpoint(
        'get',
        '/system/languages/options',
        {
            'success': True,
            'data': [
                {'name': 'English', 'code': 'en', 'filename': 'en.json.gz'}
            ],
        },
    )

    result = mock_client.system.general.get_languages()

    assert result[0].code == 'en'


@pytest.mark.unit
@responses.activate
def test_system_device_status_operations(mock_client):
    responses_by_path = {
        '/system/device/status': {
            'mnfinfo': {'name': 'RUTX11', 'macEth': '001E424F9563'},
            'ports': [
                {
                    'mac': '20:97:27:85:08:C8',
                    'num': 0,
                    'name': 'LAN',
                    'position': 1,
                }
            ],
            'static': {'fw_version': '7.19.2', 'cpu_count': 4},
            'features': {'ipv6': True},
            'board': {
                'model': {
                    'id': 'rutx11',
                    'platform': 'RUTX',
                    'name': 'RUTX11',
                },
                'hwinfo': {'wifi': True, '2_5_gigabit_port': False},
            },
        },
        '/system/device/usage/status': {
            'memory': {'ram_total': 256, 'ram_percentage': 50.5},
            'uptime': '01h 00m',
            'load': {'min1': 10, 'min5': 5, 'min15': 2},
            'uptime_seconds': 3600,
        },
        '/system/device/load/status': [[1_700_000_000, 10, 5, 2]],
        '/system/device/packages/status': [
            '/usr/lib/opkg/info/base-files.control'
        ],
        '/system/device/parameters/status': [
            {
                'id': 'g7',
                'type': 'io',
                'description': 'Relay',
                'block_pins': [5, 10],
            }
        ],
    }
    for index, (path, data) in enumerate(responses_by_path.items()):
        mock_endpoint(
            'get',
            path,
            {'success': True, 'data': data},
            include_login=index == 0,
        )

    status = mock_client.system.device.get_status()
    usage = mock_client.system.device.get_usage_status()
    load = mock_client.system.device.get_load_status()
    packages = mock_client.system.device.get_packages_status()
    parameters = mock_client.system.device.get_parameters_status()

    assert status.static.fw_version == '7.19.2'
    assert status.ports[0].num == 0
    assert status.ports[0].position == 1
    assert status.board.hwinfo.two_5_gigabit_port is False
    assert usage.memory.ram_total == 256
    assert load[0][1] == 10
    assert packages[0].endswith('.control')
    assert parameters[0].type == DeviceParameterType.IO
