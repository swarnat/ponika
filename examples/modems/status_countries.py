from examples.config import connection

for country in connection.modems.status.get_countries():
    print(country)
