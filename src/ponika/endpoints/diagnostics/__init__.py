from typing import TYPE_CHECKING

from ponika.endpoints.diagnostics.actions import ActionsEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class DiagnosticsEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.actions = ActionsEndpoint(client)
