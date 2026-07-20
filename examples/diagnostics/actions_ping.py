from examples.config import connection
from ponika.endpoints.diagnostics.actions import PingPayload
from ponika.endpoints.diagnostics.enums import DiagnosticsIpProtocol

result = connection.diagnostics.actions.ping(
    PingPayload(
        host='example.com',
        proto=DiagnosticsIpProtocol.IPV4,
    )
)

print(result.response)

"""
# Reachable
# python -m examples.diagnostics.actions_ping

PING example.com (172.66.147.243): 56 data bytes
64 bytes from 172.66.147.243: seq=0 ttl=54 time=52.486 ms
64 bytes from 172.66.147.243: seq=1 ttl=54 time=34.701 ms
64 bytes from 172.66.147.243: seq=2 ttl=54 time=44.864 ms
64 bytes from 172.66.147.243: seq=3 ttl=54 time=27.868 ms
64 bytes from 172.66.147.243: seq=4 ttl=54 time=25.152 ms

--- example.com ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 25.152/37.014/52.486 ms

# Not reachable
# python -m examples.diagnostics.actions_ping

PING 1.2.3.4 (1.2.3.4): 56 data bytes

--- 1.2.3.4 ping statistics ---
5 packets transmitted, 0 packets received, 100% packet loss
"""
