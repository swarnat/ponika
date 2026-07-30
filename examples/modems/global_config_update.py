from examples.config import connection
from ponika.endpoints.modems.global_config import (
    ModemGlobalConfigUpdatePayload,
)

config = connection.modems.global_config.update(
    '1-1', ModemGlobalConfigUpdatePayload(flight_mode=False)
)
print(config)
