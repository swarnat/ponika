from pydantic import field_validator, model_validator

from ponika.endpoints import Endpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import BaseModel, BasePayload


class ChangePasswordFirstLoginPayload(BasePayload):
    password: str
    password_confirm: str

    @field_validator('password', 'password_confirm')
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('password must contain at least 8 characters')
        if not any(character.islower() for character in value):
            raise ValueError('password must contain a lowercase character')
        if not any(character.isupper() for character in value):
            raise ValueError('password must contain an uppercase character')
        if not any(character.isdigit() for character in value):
            raise ValueError('password must contain a number')
        return value

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError('password and password_confirm must match')
        return self


class SystemActionResponse(BaseModel):
    pass


class ActionsEndpoint(Endpoint):
    def change_password_first_login(
        self, payload: ChangePasswordFirstLoginPayload
    ) -> None:
        response = self._client._post_data(
            endpoint='/system/actions/change_password_firstlogin',
            data_model=SystemActionResponse,
            params=payload,
        )
        if not response.success:
            raise TeltonikaApiException(response.errors)

    def reboot(self) -> None:
        response = self._client._post(
            endpoint='/system/actions/reboot',
            data_model=SystemActionResponse,
        )
        if not response.success:
            raise TeltonikaApiException(response.errors)
