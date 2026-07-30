from examples.config import connection
from ponika.endpoints.modems.actions import ExecAtPayload

print(
    connection.modems.actions.exec_at('1-1', ExecAtPayload(command='AT+CSQ'))
)
