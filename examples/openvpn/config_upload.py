from examples.config import connection

# Create the `vpn0` section first with config_create.py, then upload the custom
# configuration. The upload endpoint switches the section to custom mode.
response = connection.openvpn.config.upload_config(
    item_id='vpn0',
    file_path='/path/to/client.ovpn',
)

print(type(response))
print(response)
