from examples.config import connection
from ponika.endpoints.openvpn.config import OpenvpnConfigCreatePayload
from ponika.endpoints.openvpn.enums import (
    OpenvpnConfiguration,
    OpenvpnDevice,
    OpenvpnType,
)

response = connection.openvpn.config.create_with_config_upload(
    OpenvpnConfigCreatePayload(
        enable=False,
        type=OpenvpnType.CLIENT,
        name='vpn0',
        dev=OpenvpnDevice.TUN,
        enable_custom=True,
        configuration=OpenvpnConfiguration.CUSTOM,
    ),
    file_path='/path/to/client.ovpn',
)

print(type(response))
print(response.created)
print(response.upload)
print(response.config)
