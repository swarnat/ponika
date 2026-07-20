from examples.config import connection
from ponika.endpoints.diagnostics.actions import NslookupPayload

result = connection.diagnostics.actions.nslookup(
    NslookupPayload(host='1.1.1.1')
)

print(result.response)
