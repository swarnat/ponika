from examples.config import connection

from ponika.endpoints.wireless.interfaces import WirelessInterfaceDefinition

response = connection.wireless.interfaces.get_status()

print(type(response))
print(response)

response = connection.wireless.interfaces.get_status(1)

print(type(response))
print(response)