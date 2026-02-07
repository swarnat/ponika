import pprint
from examples.config import connection

from ponika.endpoints.wireless.interfaces import WirelessInterfaceDefinition

newInterface = WirelessInterfaceDefinition(
    key="Wifi-Key", 
    ssid="Example-SSID"
)
response = connection.wireless.interfaces.create(newInterface)

print(type(response))
pprint.pprint(response)