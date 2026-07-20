from examples.config import connection
from ponika.endpoints.system.buttons import ButtonUpdatePayload

print(
    connection.system.buttons.update_bulk(
        [ButtonUpdatePayload(id='reset', min='3', max='8', enabled=True)]
    )
)
