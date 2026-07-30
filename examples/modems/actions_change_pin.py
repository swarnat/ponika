from examples.config import connection
from ponika.endpoints.modems.actions import ChangePinPayload

print(
    connection.modems.actions.change_pin(
        '1-1', ChangePinPayload(pin='1234', new_pin='4321')
    )
)
