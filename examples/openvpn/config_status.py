from examples.config import connection

response = connection.openvpn.config.get_status()

print(type(response))
print(response)
