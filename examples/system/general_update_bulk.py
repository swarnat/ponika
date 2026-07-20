from examples.config import connection
from ponika.endpoints.system.general import GeneralUpdatePayload

print(
    connection.system.general.update_bulk(
        [GeneralUpdatePayload(id='general', notifications_enabled=True)]
    )
)
