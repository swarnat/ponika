from examples.config import connection
from ponika.endpoints.wireless.actions import WirelessJoinPayload

interface = connection.wireless.actions.join(
    WirelessJoinPayload(
        device='radio0',
        ssid='Example WiFi',
        password='replace-with-wifi-password',
    )
)

print(interface)
