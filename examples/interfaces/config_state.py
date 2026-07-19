from examples.config import connection
from ponika.config import PonikaConfig
from ponika.endpoints.interfaces.interfaces import InterfaceAreaType, InterfaceMode


interface = connection.interfaces.create_model(
    area_type=InterfaceAreaType.LAN,
    id='guest',
)
interface.name = 'Guest LAN'
interface.enabled = True
interface.proto = 'static'
interface.mode = InterfaceMode.STATIC
interface.ipaddr = '192.168.50.1'
interface.netmask = '255.255.255.0'
interface.ifname = ['eth0.50']

desired_config = PonikaConfig(interfaces=[interface])

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
