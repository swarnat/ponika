"""Unit tests for diagnostics action endpoints."""

import json

import pytest
import responses
from pydantic import ValidationError

from ponika.endpoints.diagnostics.actions import (
    NslookupPayload,
    PingPayload,
    TraceroutePayload,
)
from ponika.endpoints.diagnostics.enums import DiagnosticsIpProtocol
from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


@pytest.mark.unit
@responses.activate
@pytest.mark.parametrize(
    ('action', 'payload', 'expected_data'),
    [
        (
            'nslookup',
            NslookupPayload(host='example.com'),
            {'host': 'example.com'},
        ),
        (
            'ping',
            PingPayload(
                host='192.0.2.1',
                proto=DiagnosticsIpProtocol.IPV4,
            ),
            {'host': '192.0.2.1', 'proto': 'ipv4'},
        ),
        (
            'traceroute',
            TraceroutePayload(
                host='2001:db8::1',
                proto=DiagnosticsIpProtocol.IPV6,
            ),
            {'host': '2001:db8::1', 'proto': 'ipv6'},
        ),
    ],
)
def test_diagnostics_action(mock_client, action, payload, expected_data):
    mock_endpoint(
        'post',
        f'/diagnostics/actions/{action}',
        {'success': True, 'data': {'response': f'{action} output'}},
    )

    result = getattr(mock_client.diagnostics.actions, action)(payload)

    assert result.response == f'{action} output'
    assert json.loads(responses.calls[-1].request.body) == {
        'data': expected_data
    }


@pytest.mark.parametrize(
    'host',
    ['', 'invalid host', '-invalid.example', 'invalid-.example', 'a' * 254],
)
def test_diagnostics_host_rejects_invalid_value(host):
    with pytest.raises(ValidationError, match='host'):
        NslookupPayload(host=host)


def test_diagnostics_protocol_rejects_unknown_value():
    with pytest.raises(ValidationError, match='proto'):
        PingPayload(host='example.com', proto='ipx')


@pytest.mark.unit
@responses.activate
@pytest.mark.parametrize(
    ('action', 'payload'),
    [
        ('nslookup', NslookupPayload(host='example.com')),
        (
            'ping',
            PingPayload(host='example.com', proto=DiagnosticsIpProtocol.IPV4),
        ),
        (
            'traceroute',
            TraceroutePayload(
                host='example.com', proto=DiagnosticsIpProtocol.IPV6
            ),
        ),
    ],
)
def test_diagnostics_action_error_raises(mock_client, action, payload):
    mock_error_response(
        'post',
        f'/diagnostics/actions/{action}',
        error_code=422,
        error_message=f'Failed to run {action}',
        error_source='diagnostics',
    )

    with pytest.raises(TeltonikaApiException):
        getattr(mock_client.diagnostics.actions, action)(payload)
