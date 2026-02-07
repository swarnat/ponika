from examples.config import connection

from ponika.endpoints.wireless.interfaces import WirelessInterfaceDefinition

response = connection.wireless.interfaces.get_config(1)

response.data.enabled = False

response = connection.wireless.interfaces.update(response.data)

print(type(response))
print(response)