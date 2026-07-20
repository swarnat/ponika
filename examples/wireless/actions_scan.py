from examples.config import connection
from ponika.endpoints.wireless.actions import WirelessScanPayload

networks = connection.wireless.actions.scan(
    WirelessScanPayload(device='radio0')
)

for network in networks:
    print(network)
