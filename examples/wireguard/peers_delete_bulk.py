from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerBulkDeletePayload

response = connection.wireguard.peers.delete_bulk(
    WireguardPeerBulkDeletePayload(
        id='wg0',
        peers_ids=['peer1', 'peer2'],
    )
)

print(type(response))
print(response)
