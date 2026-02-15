from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerBulkUpdatePayload

response = connection.wireguard.peers.update_bulk(
    [
        WireguardPeerBulkUpdatePayload(
            id='wg0',
            peers_id='peer1',
            public_key='p' * 44,
            allowed_ips=['10.10.0.2/32'],
        ),
        WireguardPeerBulkUpdatePayload(
            id='wg0',
            peers_id='peer2',
            public_key='q' * 44,
            allowed_ips=['10.10.0.4/32'],
        ),
    ]
)

print(type(response))
print(response)
