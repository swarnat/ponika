from examples.config import connection
from ponika.endpoints.system.buttons import ButtonUpdatePayload

target_endpoint = connection.system.buttons
response = target_endpoint.get_config()

if len(response) == 0:
    print('No Buttons found')
else:
    first_item_id = response[0].id

    print(
        connection.system.buttons.update(
            ButtonUpdatePayload(
                id=first_item_id, min='1', max='3', enabled=False
            )
        )
    )
