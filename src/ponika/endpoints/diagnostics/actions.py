from ipaddress import ip_address
import re

from pydantic import field_validator

from ponika.endpoints import Endpoint
from ponika.endpoints.diagnostics.enums import DiagnosticsIpProtocol
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel, BasePayload


HOSTNAME_LABEL_PATTERN = re.compile(
    r'^(?!-)[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$',
    re.IGNORECASE,
)


class DiagnosticsHostPayload(BasePayload):
    host: str

    @field_validator('host')
    @classmethod
    def validate_host(cls, value: str) -> str:
        host = value.strip()
        if not host:
            raise ValueError('host must not be empty')

        try:
            ip_address(host)
            return host
        except ValueError:
            pass

        hostname = host[:-1] if host.endswith('.') else host
        if len(hostname) > 253 or not all(
            HOSTNAME_LABEL_PATTERN.fullmatch(label)
            for label in hostname.split('.')
        ):
            raise ValueError('host must be a valid IP address or hostname')

        return host


class DiagnosticsProtocolHostPayload(DiagnosticsHostPayload):
    proto: DiagnosticsIpProtocol


class NslookupPayload(DiagnosticsHostPayload):
    pass


class PingPayload(DiagnosticsProtocolHostPayload):
    pass


class TraceroutePayload(DiagnosticsProtocolHostPayload):
    pass


class DiagnosticsActionResponse(BaseModel):
    response: str


class ActionsEndpoint(Endpoint):
    def nslookup(self, payload: NslookupPayload) -> DiagnosticsActionResponse:
        return self._run('nslookup', payload)

    def ping(self, payload: PingPayload) -> DiagnosticsActionResponse:
        return self._run('ping', payload)

    def traceroute(
        self, payload: TraceroutePayload
    ) -> DiagnosticsActionResponse:
        return self._run('traceroute', payload)

    def _run(
        self,
        action: str,
        payload: DiagnosticsHostPayload,
    ) -> DiagnosticsActionResponse:
        response = self._client._post_data(
            endpoint=f'/diagnostics/actions/{action}',
            data_model=DiagnosticsActionResponse,
            params=payload,
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data
