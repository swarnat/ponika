from examples.config import connection


response = connection.interfaces.get_config('lan')

print(type(response))
print(response)
