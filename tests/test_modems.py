"""Unit tests for all `/modems` endpoints."""

import json
from typing import Any

import pytest
import responses
from pydantic import ValidationError

from ponika.endpoints.modems.actions import (
    ChangePinPayload,
    ExecAtPayload,
    PinLockPayload,
    SendUssdPayload,
    SimUnblockPayload,
    SimUnlockPayload,
)
from ponika.endpoints.modems.enums import (
    ModemName,
    NetworkType,
    OperatorStatus,
    UssdState,
)
from ponika.endpoints.modems.global_config import (
    ModemGlobalConfigUpdatePayload,
)
from ponika.endpoints.modems.sim_cards import (
    SimCardBulkUpdatePayload,
    SimCardUpdatePayload,
)
from ponika.endpoints.modems.status import (
    ModemOfflineStatus,
    ModemOnlineStatus,
    ModemStatusError,
)
from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


MODEM_ID = '1-1'

ONLINE_STATUS = {
    'id': MODEM_ID,
    'imei': '123456789012345',
    'model': 'TRM250',
    'mode': 1,
    'builtin': True,
    'cell_info': [{'mcc': '262', 'nr-arfcn': '640000'}],
    'ca_signal': [],
}
REAL_ONLINE_STATUS = {
    'operators_scan': True,
    'pinleft': 3,
    'operator_state': 'Registered, home',
    'wwan_gnss_conflict': False,
    'sim_count': 2,
    'modem_state_id': 1,
    'pinstate': 'Inserted',
    'manufacturer': 'Quectel',
    'mobile_dfota': False,
    'auto_2g_bands': False,
    'volte_supported': True,
    'state_id': 1,
    'sim_switch_enabled': False,
    'conntype': '4G (LTE); VoLTE',
    'state': 'Connected',
    'temperature': 59,
    'serial': 'MPX25FG05005711',
    'esim_bootstrap': False,
    'imsi': '262011530302216',
    'is_busy': 0,
    'cellid': '30431492',
    'mode': 0,
    'ipv6': True,
    'primary': True,
    'builtin': True,
    'simstate_id': 0,
    'netstate_id': 1,
    'simstate': 'Inserted',
    'txbytes': 1006117231,
    'nr5g_sa_disabled': False,
    'rsrp': -72,
    'rxbytes': 676269096,
    'cell_info': [
        {
            'lac': 'N/A',
            'mcc': '262',
            'rsrp': 'N/A',
            'ue_state': 3,
            'bandwidth': '10',
            'sinr': 'N/A',
            'rsrq': 'N/A',
            'nr-arfcn': 'N/A',
            'cellid': '30431492',
            'mnc': '01',
            'earfcn': 3749,
            'uarfcn': 'N/A',
            'arfcn': 'N/A',
            'pcid': 457,
            'tac': '16550',
        }
    ],
    'mobile_stage': 19,
    'cfg_version': '20.200.20.200',
    'data_conn_state_id': 1,
    'oper': 'Telekom.de',
    'csd': False,
    'operator': 'Telekom.de',
    'version': 'EC25ECGAR06A16M1G',
    'model': 'EC25-EC',
    'busy_state': 'Idle',
    'imei': '865828069668075',
    'data_off': False,
    'active_sim': 1,
    'busy_state_id': 1,
    'low_signal_reconnect': True,
    'pinstate_id': 1,
    'rssi': -48,
    'name': 'Internal modem',
    'service_modes': {
        '4G': ['lte_b1', 'lte_b3'],
        '3G': ['wcdma_900', 'wcdma_2100'],
        '2G': ['gsm_900', 'gsm_1800'],
    },
    'id': MODEM_ID,
    'auto_3g_bands': False,
    'data_conn_state': 'Connected',
    'ca_signal': [],
    'baudrate': 115200,
    'rsrq': -7,
    'provider': 'Telekom.de',
    'framed_routing': False,
    'band': 'LTE B8',
    'lac': 'N/A',
    'multi_apn': True,
    'operator_state_id': 1,
    'auto_5g_mode': False,
    'sc_band_av': 'Inactive',
    'netstate': 'Registered, home',
    'sinr': 21,
    'ntype': 'LTE',
    'tac': '16550',
    'iccid': '89490200001859724919',
    'dynamic_mtu': True,
    'no_ussd': False,
    'volte': True,
    'pukleft': 10,
    'signal': -48,
}
OFFLINE_STATUS = {
    'id': '2-1',
    'name': 'Secondary modem',
    'offline': '1',
    'blocked': '0',
    'disabled': '0',
}
APN = {
    'id': 1,
    'password': '',
    'apn': 'internet',
    'user': '',
    'carrier': 'default',
    'auth': 'none',
    'pdptype': '0',
}
SIGNAL = {
    'timestamp': '2026-07-29T20:00:00Z',
    'network_type': 19,
    'band': 'LTE B3',
    'rssi': -65,
    'rsrp': -92,
}
OPERATOR = {
    'net_access_type': '4G',
    'status_code': 2,
    'status': 'Current',
    'op_name': 'Example Telecom',
    'short_name': 'Example',
    'num_name': '26201',
}
SIM_CONFIG = {
    'id': '1',
    'modem': MODEM_ID,
    'primary': '1',
    'deny_roaming': '0',
    'volte': 'auto',
    'service': 'lte_pref',
    'band': 'auto',
    'gsm': [],
    'umts': [],
    'lte': ['lte_b3'],
    'lte_nb': [],
    'nr5g': [],
    'nr5g_sa': [],
    'signal_reset_enabled': '1',
    'signal_reset_threshold': '-110',
    'signal_reset_timeout': '60',
    'operlist': '0',
    'opermode': 'whitelist',
    'operlist_name': '',
    'enable_sms_limit': '0',
    'sms_limit_num': '100',
    'sms_limit': 'day',
    'period': '0',
    'operator': 'auto',
}


def sim_payload(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        'signal_reset_threshold': '-110',
        'signal_reset_timeout': '60',
        'opermode': 'whitelist',
        'operlist_name': '',
        'sms_limit_num': '100',
        'sms_limit': 'day',
        'period': '0',
    }
    data.update(overrides)
    return data


def last_request_json() -> dict:
    body = responses.calls[-1].request.body
    assert body is not None
    return json.loads(body)


@pytest.mark.unit
@responses.activate
def test_modem_status_list_and_backward_compatible_shortcut(mock_client):
    mock_endpoint(
        'get',
        '/modems/status',
        {'success': True, 'data': [ONLINE_STATUS, OFFLINE_STATUS]},
    )

    result = mock_client.modems.get_status()

    assert isinstance(result[0], ModemOnlineStatus)
    assert isinstance(result[1], ModemOfflineStatus)
    assert result[1].offline is True
    assert result[1].blocked is False
    assert result[1].name is ModemName.SECONDARY
    assert result[0].cell_info[0].nr_arfcn == '640000'


@pytest.mark.unit
@responses.activate
def test_modem_status_by_id(mock_client):
    mock_endpoint(
        'get',
        f'/modems/status/{MODEM_ID}',
        {'success': True, 'data': ONLINE_STATUS},
    )

    result = mock_client.modems.status.get_status(MODEM_ID)

    assert isinstance(result, ModemOnlineStatus)
    assert result.id == MODEM_ID


@pytest.mark.unit
@responses.activate
def test_modem_real_device_online_status_is_not_parsed_as_offline(mock_client):
    mock_endpoint(
        'get',
        '/modems/status',
        {'success': True, 'data': [REAL_ONLINE_STATUS]},
    )

    result = mock_client.modems.status.get_status()

    assert isinstance(result[0], ModemOnlineStatus)
    assert result[0].cell_info[0].sinr == 'N/A'


@pytest.mark.unit
@responses.activate
def test_invalid_online_status_does_not_fall_back_to_offline(mock_client):
    invalid_online = {**REAL_ONLINE_STATUS, 'mode': 99}
    mock_endpoint(
        'get',
        '/modems/status',
        {'success': True, 'data': [invalid_online]},
    )

    with pytest.raises(ValidationError, match='mode'):
        mock_client.modems.status.get_status()


@pytest.mark.unit
@responses.activate
def test_modem_apns_list_includes_per_modem_error(mock_client):
    error = {'code': 1, 'error': 'APN data not found', 'modem': '2-1'}
    mock_endpoint(
        'get',
        '/modems/apns/status',
        {'success': True, 'data': [{'modem': MODEM_ID, 'apns': [APN]}, error]},
    )

    result = mock_client.modems.status.get_apns()

    assert result[0].apns[0].apn == 'internet'
    assert isinstance(result[1], ModemStatusError)


@pytest.mark.unit
@responses.activate
def test_modem_apns_by_id(mock_client):
    mock_endpoint(
        'get',
        f'/modems/apns/status/{MODEM_ID}',
        {'success': True, 'data': [APN]},
    )

    result = mock_client.modems.status.get_apns(MODEM_ID)

    assert result[0].auth.value == 'none'
    assert result[0].pdptype.value == '0'


@pytest.mark.unit
@responses.activate
def test_modem_signal_list(mock_client):
    mock_endpoint(
        'get',
        '/modems/signal/status',
        {'success': True, 'data': [{'modem': MODEM_ID, 'signal': [SIGNAL]}]},
    )

    result = mock_client.modems.status.get_signal()

    assert result[0].signal[0].rsrp == -92


@pytest.mark.unit
@responses.activate
def test_modem_signal_by_id(mock_client):
    mock_endpoint(
        'get',
        f'/modems/signal/status/{MODEM_ID}',
        {'success': True, 'data': [SIGNAL]},
    )

    result = mock_client.modems.status.get_signal(MODEM_ID)

    assert result[0].network_type is NetworkType.TYPE_19


@pytest.mark.unit
@responses.activate
def test_modem_scan_list(mock_client):
    mock_endpoint(
        'get',
        '/modems/scan/status',
        {
            'success': True,
            'data': [
                {
                    'modem': MODEM_ID,
                    'last_scan': 'now',
                    'operators': [OPERATOR],
                }
            ],
        },
    )

    result = mock_client.modems.status.get_scan()

    assert result[0].operators[0].status is OperatorStatus.CURRENT


@pytest.mark.unit
@responses.activate
def test_modem_scan_by_id(mock_client):
    mock_endpoint(
        'get',
        f'/modems/scan/status/{MODEM_ID}',
        {
            'success': True,
            'data': {'last_scan': 'now', 'operators': [OPERATOR]},
        },
    )

    result = mock_client.modems.status.get_scan(MODEM_ID)

    assert result.last_scan == 'now'


@pytest.mark.unit
@responses.activate
def test_modem_countries(mock_client):
    mock_endpoint(
        'get',
        '/modems/countries/status',
        {'success': True, 'data': [{'mcc': '262', 'country': 'Germany'}]},
    )

    result = mock_client.modems.status.get_countries()

    assert result[0].country == 'Germany'


@pytest.mark.unit
@responses.activate
def test_modem_global_config_get(mock_client):
    mock_endpoint(
        'get',
        f'/modems/{MODEM_ID}/global',
        {'success': True, 'data': {'modem': MODEM_ID, 'flight_mode': '0'}},
    )

    result = mock_client.modems.global_config.get(MODEM_ID)

    assert result.flight_mode is False


@pytest.mark.unit
@responses.activate
def test_modem_global_config_update_serializes_bool(mock_client):
    mock_endpoint(
        'put',
        f'/modems/{MODEM_ID}/global',
        {'success': True, 'data': {'modem': MODEM_ID, 'flight_mode': '1'}},
    )

    result = mock_client.modems.global_config.update(
        MODEM_ID, ModemGlobalConfigUpdatePayload(flight_mode=True)
    )

    assert result.flight_mode is True
    assert last_request_json() == {'data': {'flight_mode': '1'}}


@pytest.mark.unit
@responses.activate
def test_modem_send_ussd(mock_client):
    mock_endpoint(
        'post',
        f'/modems/{MODEM_ID}/actions/send_ussd',
        {
            'success': True,
            'data': {'message': 'Balance: 10', 'state_id': 0, 'timestamp': 1},
        },
    )

    result = mock_client.modems.actions.send_ussd(
        MODEM_ID, SendUssdPayload(ussd='*100#')
    )

    assert result.state_id is UssdState.COMPLETE
    assert last_request_json() == {'data': {'ussd': '*100#'}}


@pytest.mark.unit
@responses.activate
def test_modem_scan_network(mock_client):
    mock_endpoint(
        'post',
        f'/modems/{MODEM_ID}/actions/scan_network',
        {'success': True, 'data': [OPERATOR]},
    )

    result = mock_client.modems.actions.scan_network(MODEM_ID)

    assert result[0].num_name == '26201'


@pytest.mark.unit
@responses.activate
@pytest.mark.parametrize('action', ['reboot', 'restart_connection'])
def test_modem_empty_actions(mock_client, action):
    mock_endpoint(
        'post', f'/modems/{MODEM_ID}/actions/{action}', {'success': True}
    )

    result = getattr(mock_client.modems.actions, action)(MODEM_ID)

    assert result is None


@pytest.mark.unit
@responses.activate
def test_modem_exec_at(mock_client):
    mock_endpoint(
        'post',
        f'/modems/{MODEM_ID}/actions/exec_at',
        {'success': True, 'data': {'response': 'OK'}},
    )

    result = mock_client.modems.actions.exec_at(
        MODEM_ID, ExecAtPayload(command='AT')
    )

    assert result.response == 'OK'


@pytest.mark.unit
@responses.activate
def test_modem_sim_unblock(mock_client):
    mock_endpoint(
        'post',
        f'/modems/{MODEM_ID}/actions/sim_unblock',
        {'success': True, 'data': {'pin:set': '1'}},
    )

    result = mock_client.modems.actions.sim_unblock(
        MODEM_ID, SimUnblockPayload(pin='1234', puk='12345678')
    )

    assert result.pin_set is True


@pytest.mark.unit
@responses.activate
def test_modem_sim_unlock(mock_client):
    mock_endpoint(
        'post', f'/modems/{MODEM_ID}/actions/sim_unlock', {'success': True}
    )

    result = mock_client.modems.actions.sim_unlock(
        MODEM_ID, SimUnlockPayload(pin='1234')
    )

    assert result is None


@pytest.mark.unit
@responses.activate
def test_modem_change_pin(mock_client):
    mock_endpoint(
        'post',
        f'/modems/{MODEM_ID}/actions/change_pin',
        {'success': True, 'data': {'new_pin:set': '1'}},
    )

    result = mock_client.modems.actions.change_pin(
        MODEM_ID, ChangePinPayload(pin='1234', new_pin='4321')
    )

    assert result.new_pin_set is True


@pytest.mark.unit
@responses.activate
def test_modem_pin_lock_serializes_bool(mock_client):
    mock_endpoint(
        'post', f'/modems/{MODEM_ID}/actions/pin_lock', {'success': True}
    )

    mock_client.modems.actions.pin_lock(
        MODEM_ID, PinLockPayload(enabled=False, pin='1234')
    )

    assert last_request_json() == {'data': {'enabled': '0', 'pin': '1234'}}


@pytest.mark.unit
@responses.activate
def test_modem_sim_cards_get_config(mock_client):
    mock_endpoint(
        'get',
        f'/modems/{MODEM_ID}/sim_cards/config',
        {'success': True, 'data': [SIM_CONFIG]},
    )

    result = mock_client.modems.sim_cards.get_config(MODEM_ID)

    assert result[0].primary is True
    assert result[0].deny_roaming is False
    assert result[0].lte is not None
    assert result[0].lte[0].value == 'lte_b3'


@pytest.mark.unit
@responses.activate
def test_modem_sim_card_get_config_by_id(mock_client):
    mock_endpoint(
        'get',
        f'/modems/{MODEM_ID}/sim_cards/config/1',
        {'success': True, 'data': SIM_CONFIG},
    )

    result = mock_client.modems.sim_cards.get_config(MODEM_ID, '1')

    assert result.id == '1'


@pytest.mark.unit
@responses.activate
def test_modem_sim_card_update(mock_client):
    mock_endpoint(
        'put',
        f'/modems/{MODEM_ID}/sim_cards/config/1',
        {'success': True, 'data': SIM_CONFIG},
    )
    payload = SimCardUpdatePayload(
        **sim_payload(primary=True, deny_roaming=False)
    )

    result = mock_client.modems.sim_cards.update(MODEM_ID, '1', payload)

    assert result.id == '1'
    body = last_request_json()
    assert body['data']['primary'] == '1'
    assert body['data']['deny_roaming'] == '0'
    assert 'gsm' not in body['data']


@pytest.mark.unit
@responses.activate
def test_modem_sim_cards_bulk_update(mock_client):
    mock_endpoint(
        'put',
        f'/modems/{MODEM_ID}/sim_cards/config',
        {'success': True, 'data': [SIM_CONFIG]},
    )
    payload = SimCardBulkUpdatePayload(
        **sim_payload(id='1', primary=True, nr5g_sa=['78'])
    )

    result = mock_client.modems.sim_cards.update_bulk(MODEM_ID, [payload])

    assert result[0].id == '1'
    request_item = last_request_json()['data'][0]
    assert request_item['id'] == '1'
    assert request_item['nr5g_sa'] == ['78']


def test_modem_sim_card_operator_number_validation():
    with pytest.raises(ValidationError, match='5 or 6'):
        SimCardUpdatePayload(**sim_payload(opernum='1234'))


@pytest.mark.unit
@responses.activate
def test_modem_api_error_raises(mock_client):
    mock_error_response(
        'get',
        '/modems/status',
        error_code=404,
        error_message='No modems found',
        error_source='modems',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.modems.status.get_status()
