from examples.config import connection
from ponika.endpoints.openvpn.config import OpenvpnConfigCreatePayload
from ponika.endpoints.openvpn.enums import OpenvpnDevice, OpenvpnType

response = connection.openvpn.config.create(
    OpenvpnConfigCreatePayload(
        enable=False,
        type=OpenvpnType.CLIENT,
        name='vpn0',
        dev=OpenvpnDevice.TUN,
    )
)

print(type(response))
print(response)
