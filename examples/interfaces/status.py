from examples.config import connection


response = connection.interfaces.get_status()

print(type(response))
print(response)
