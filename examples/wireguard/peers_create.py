from examples.config import connection
from ponika.endpoints.wireguard.peers import WireguardPeerCreatePayload

response = connection.wireguard.peers.create(
    WireguardPeerCreatePayload(
        id='wg0',
        peer_id='peer1',
        public_key='p' * 44,
        allowed_ips=['10.10.0.2/32'],
        route_allowed_ips=True,
    )
)

print(type(response))
print(response)
