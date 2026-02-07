from examples.config import connection

from ponika.endpoints.wireless.interfaces import WirelessInterfaceDefinition

response = connection.wireless.interfaces.delete(1)

print(type(response))
print(response)