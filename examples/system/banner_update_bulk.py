from examples.config import connection
from ponika.endpoints.system.banner import BannerUpdatePayload

print(
    connection.system.banner.update_bulk(
        [BannerUpdatePayload(id='login', enabled=True, title='Notice')]
    )
)
