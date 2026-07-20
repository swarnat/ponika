from examples.config import connection
from ponika.endpoints.openvpn.tls_clients import OpenvpnTlsClientCreatePayload

response = connection.openvpn.tls_clients.config('vpn0').create(
    OpenvpnTlsClientCreatePayload(
        id='client1',
        name='Laptop',
        common_name='laptop.example',
        covered_network=['192.168.10.0/24'],
    )
)

print(type(response))
print(response)
