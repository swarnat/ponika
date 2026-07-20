from examples.config import connection

response = connection.openvpn.tls_clients.config('vpn0').get_config()

print(type(response))
print(response)
