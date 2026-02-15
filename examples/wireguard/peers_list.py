from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerGetPayload

response = connection.wireguard.peers.get_config(
    WireguardPeerGetPayload(id='wg0')
)

print(type(response))
print(response)
