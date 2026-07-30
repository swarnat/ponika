from examples.config import connection
from ponika.endpoints.modems.actions import PinLockPayload

connection.modems.actions.pin_lock(
    '1-1', PinLockPayload(enabled=True, pin='1234')
)
