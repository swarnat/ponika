from examples.config import connection


response = connection.interfaces.get_config()

print(type(response))
print(response)
