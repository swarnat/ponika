from examples.config import connection

for signal in connection.modems.status.get_signal('1-1'):
    print(signal)
