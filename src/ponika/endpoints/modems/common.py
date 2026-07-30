from typing import TypeVar

from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel

T = TypeVar('T')


class EmptyModemActionResponse(BaseModel):
    pass


def response_data(response: ApiResponse[T]) -> T:
    """Return successful response data or raise the device API error."""
    if not response.success or response.data is None:
        raise TeltonikaApiException(response.errors)
    return response.data


def ensure_success(response: ApiResponse[object]) -> None:
    """Validate an action response that intentionally has no data."""
    if not response.success:
        raise TeltonikaApiException(response.errors)
