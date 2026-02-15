from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerUpdatePayload

response = connection.wireguard.peers.update(
    WireguardPeerUpdatePayload(
        id='wg0',
        peers_id='peer1',
        public_key='p' * 44,
        allowed_ips=['10.10.0.3/32'],
        route_allowed_ips=False,
    )
)

print(type(response))
print(response)
