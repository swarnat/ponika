from examples.config import connection

response = connection.openvpn.tls_clients.config('vpn0').delete('client1')

print(type(response))
print(response)
