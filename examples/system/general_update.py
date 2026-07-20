from examples.config import connection
from ponika.endpoints.system.general import GeneralUpdatePayload

print(
    connection.system.general.update(
        GeneralUpdatePayload(
            id='general',
            hostname='router-ponika',
        )
    )
)
