from examples.config import connection
from ponika.endpoints.interfaces.interfaces import InterfaceAreaType, InterfaceMode


new_interface = connection.interfaces.create_model(area_type=InterfaceAreaType.LAN)
new_interface.id = 'guest'
new_interface.name = 'Guest LAN'
new_interface.enabled = True
new_interface.proto = 'static'
new_interface.mode = InterfaceMode.STATIC
new_interface.ipaddr = '192.168.50.1'
new_interface.netmask = '255.255.255.0'
new_interface.ifname = ['eth0.50']

response = connection.interfaces.create(new_interface)

print(type(response))
print(response)
