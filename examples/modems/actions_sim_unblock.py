from examples.config import connection
from ponika.endpoints.modems.actions import SimUnblockPayload

print(
    connection.modems.actions.sim_unblock(
        '1-1', SimUnblockPayload(pin='1234', puk='12345678')
    )
)
