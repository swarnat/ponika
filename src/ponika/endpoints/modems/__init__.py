from typing import TYPE_CHECKING

from ponika.endpoints.modems.actions import ModemActionsEndpoint
from ponika.endpoints.modems.global_config import ModemGlobalConfigEndpoint
from ponika.endpoints.modems.sim_cards import ModemSimCardsEndpoint
from ponika.endpoints.modems.status import ModemStatus, ModemStatusEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class ModemsEndpoint:
    """Entry point for modem status, configuration, and actions."""

    def __init__(self, client: 'PonikaClient') -> None:
        self._client = client
        self.status = ModemStatusEndpoint(client)
        self.global_config = ModemGlobalConfigEndpoint(client)
        self.actions = ModemActionsEndpoint(client)
        self.sim_cards = ModemSimCardsEndpoint(client)

    def get_status(
        self, modem_id: str | None = None
    ) -> ModemStatus | list[ModemStatus]:
        """Backward-compatible shortcut for :meth:`status.get_status`."""
        if modem_id is None:
            return self.status.get_status()
        return self.status.get_status(modem_id)
