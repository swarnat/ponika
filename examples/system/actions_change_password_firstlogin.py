from examples.config import connection
from ponika.endpoints.system.actions import ChangePasswordFirstLoginPayload

connection.system.actions.change_password_first_login(
    ChangePasswordFirstLoginPayload(
        password='Updated-passw0rd',
        password_confirm='Updated-passw0rd',
    )
)
print('Password changed')
