from examples.config import connection
from ponika.endpoints.modems.sim_cards import SimCardUpdatePayload

payload = SimCardUpdatePayload(
    primary=True,
    signal_reset_threshold='-110',
    signal_reset_timeout='60',
    opermode='whitelist',
    operlist_name='',
    sms_limit_num='100',
    sms_limit='day',
    period='0',
)
print(connection.modems.sim_cards.update('1-1', '1', payload))
