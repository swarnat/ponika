from examples.config import connection
from ponika.endpoints.modems.actions import SendUssdPayload

print(
    connection.modems.actions.send_ussd('1-1', SendUssdPayload(ussd='*100#'))
)
