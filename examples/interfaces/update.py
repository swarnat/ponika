from examples.config import connection


response = connection.interfaces.get_config()

update_interface = None

for interface in response:
    update_interface = interface
    break

if update_interface is None:
    print('No interface found to update')
else:
    print(f'Update interface with id {update_interface.id}')

    update_payload = connection.interfaces.config_to_update_payload(
        update_interface
    )
    update_payload.enabled = True
    update_payload.ipaddr = '192.168.2.1'
    update_payload.netmask = '255.255.255.248'
    # update_payload.metric = '1'

    response = connection.interfaces.update(update_payload)

    print(type(response))
    print(response)
