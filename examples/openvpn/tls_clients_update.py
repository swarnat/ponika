from examples.config import connection
from ponika.endpoints.openvpn.tls_clients import OpenvpnTlsClientUpdatePayload

response = connection.openvpn.tls_clients.config('vpn0').update(
    OpenvpnTlsClientUpdatePayload(
        id='client1',
        local_ip='172.16.1.6',
        remote_ip='172.16.1.5',
    )
)

print(type(response))
print(response)
