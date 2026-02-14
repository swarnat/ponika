from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerDeletePayload

response = connection.wireguard.peers.delete(
    WireguardPeerDeletePayload(
        id="wg0",
        peers_id="peer1",
    )
)

print(type(response))
print(response)
