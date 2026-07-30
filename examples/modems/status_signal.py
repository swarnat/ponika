from examples.config import connection

for modem in connection.modems.status.get_signal():
    print(modem)
