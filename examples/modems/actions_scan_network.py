from examples.config import connection

for operator in connection.modems.actions.scan_network('1-1'):
    print(operator)
