from examples.config import connection

from ponika.endpoints.wireless.interfaces import WirelessInterfaceDefinition

response = connection.wireless.interfaces.get_config(1)

print(response)
