from examples.config import connection
from ponika.endpoints.diagnostics.actions import TraceroutePayload
from ponika.endpoints.diagnostics.enums import DiagnosticsIpProtocol

result = connection.diagnostics.actions.traceroute(
    TraceroutePayload(
        host='example.com',
        proto=DiagnosticsIpProtocol.IPV4,
    )
)

print(result.response)
