from examples.config import connection
from ponika.endpoints.system.led import LedUpdatePayload

print(
    connection.system.led.update_bulk(
        [LedUpdatePayload(id='all', enabled=False)]
    )
)
