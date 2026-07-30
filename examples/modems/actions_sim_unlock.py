from examples.config import connection
from ponika.endpoints.modems.actions import SimUnlockPayload

connection.modems.actions.sim_unlock('1-1', SimUnlockPayload(pin='1234'))
