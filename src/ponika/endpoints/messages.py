from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, List

from pydantic import field_validator

from ponika.endpoints import Endpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload

if TYPE_CHECKING:
    from ponika import PonikaClient


class MessagesStatusResponseItem(BaseModel):
    """Data model for a single message status item."""

    DEVICE_DATE_FORMAT: ClassVar[str] = '%a %b %d %H:%M:%S %Y'

    message: str
    sender: str
    id: str
    modem_id: str
    status: str
    date: datetime

    @field_validator('date', mode='before')
    @classmethod
    def parse_device_date(cls, value: object) -> object:
        """Parse the non-ISO timestamp returned by message status."""
        if isinstance(value, str):
            try:
                return datetime.strptime(value, cls.DEVICE_DATE_FORMAT)
            except ValueError:
                pass

        return value


class SendMessagePayload(BasePayload):
    number: str
    message: str
    modem: str


class SendMessageResponseData(BaseModel):
    """Data model for message send action response."""

    sms_used: int


class RemoveMessagesPayload(BasePayload):
    modem_id: str
    sms_id: List[str]


class RemoveMessagesResponseData(BaseModel):
    """Data model for remove messages action response."""

    response: str


class MessagesEndpoint(Endpoint):
    def __init__(self, client: 'PonikaClient') -> None:
        super().__init__(client)

    def read(self) -> List[MessagesStatusResponseItem]:
        """Fetch messages from the device."""
        response_model = ApiResponse[List[MessagesStatusResponseItem]]
        response = response_model.model_validate(
            self._client._get(
                '/messages/status',
            )
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def send(
        self, number: str, message: str, modem: str
    ) -> SendMessageResponseData:
        """Send a message to a recipient."""
        payload = SendMessagePayload(
            number=number,
            message=message,
            modem=modem,
        )

        response = self._client._post_data(
            endpoint='/messages/actions/send',
            data_model=SendMessageResponseData,
            params=payload,
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data

    def remove(
        self,
        modem_id: str,
        sms_ids: List[str],
    ) -> RemoveMessagesResponseData:
        """Delete selected SMS messages from a modem."""
        payload = RemoveMessagesPayload(
            modem_id=modem_id,
            sms_id=sms_ids,
        )

        response = self._client._post_data(
            endpoint='/messages/actions/remove_messages',
            data_model=RemoveMessagesResponseData,
            params=payload,
        )

        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)

        return response.data
