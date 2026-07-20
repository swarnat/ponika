from examples.config import connection

response = connection.openvpn.config.get_config()

print(type(response))
print(response)
