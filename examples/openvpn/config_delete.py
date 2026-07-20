from examples.config import connection

response = connection.openvpn.config.delete('vpn0')

print(type(response))
print(response)
