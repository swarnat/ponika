from examples.config import connection


response = connection.interfaces.get_config()

delete_interface = None

for interface in response:
    delete_interface = interface
    break

if delete_interface is None:
    print('No interface found to delete')
else:
    print(f'Delete interface with id {delete_interface.id}')

    response = connection.interfaces.delete(delete_interface.id)

    print(type(response))
    print(response)
