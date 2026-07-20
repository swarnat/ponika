from examples.config import connection
from ponika.config import (
    OpenvpnConfig,
    OpenvpnTlsClientsConfig,
    PonikaConfig,
)
from ponika.endpoints.openvpn.config import OpenvpnConfigCreatePayload
from ponika.endpoints.openvpn.enums import OpenvpnDevice, OpenvpnType
from ponika.endpoints.openvpn.tls_clients import OpenvpnTlsClientCreatePayload

openvpn_config = OpenvpnConfigCreatePayload(
    enable=False,
    type=OpenvpnType.SERVER,
    name='vpn0',
    dev=OpenvpnDevice.TUN,
)

tls_client = OpenvpnTlsClientCreatePayload(
    id='client1',
    name='Laptop',
    common_name='laptop.example',
)

desired_config = PonikaConfig(
    openvpn=OpenvpnConfig(
        config=[openvpn_config],
        tls_clients=[
            OpenvpnTlsClientsConfig(openvpn_id='vpn0', items=[tls_client])
        ],
    )
)

preview = connection.config.apply(
    desired_config,
    dry_run=True,
    delete_unmanaged=False,
)
print(preview.changes)

result = connection.config.apply(
    desired_config,
    delete_unmanaged=False,
)
print(result)
