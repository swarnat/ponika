from examples.config import connection

for modem in connection.modems.status.get_status():
    print(modem)
    print(modem.rsrp)
    print(modem.rsrq)
    print(modem.sinr)
