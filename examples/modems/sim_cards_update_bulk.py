from examples.config import connection
from ponika.endpoints.modems.sim_cards import SimCardBulkUpdatePayload

payload = SimCardBulkUpdatePayload(
    id='1',
    primary=True,
    signal_reset_threshold='-110',
    signal_reset_timeout='60',
    opermode='whitelist',
    operlist_name='',
    sms_limit_num='100',
    sms_limit='day',
    period='0',
)
for sim_card in connection.modems.sim_cards.update_bulk('1-1', [payload]):
    print(sim_card)
