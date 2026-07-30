from examples.config import connection

for apn in connection.modems.status.get_apns('1-1'):
    print(apn)
