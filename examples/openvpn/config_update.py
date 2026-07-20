from examples.config import connection
from ponika.endpoints.openvpn.config import OpenvpnConfigUpdatePayload

response = connection.openvpn.config.update(
    OpenvpnConfigUpdatePayload(
        id='vpn0',
        enable=True,
    )
)

print(type(response))
print(response)
