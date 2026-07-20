from pathlib import Path

from examples.config import connection

config_content = connection.openvpn.config.download_config('vpn0')

Path('vpn0.ovpn').write_bytes(config_content)
