from typing import Generic, TypeVar, cast

from ponika.endpoints import Endpoint
from ponika.exceptions import TeltonikaApiException
from ponika.models import ApiResponse, BaseModel, BasePayload


TConfig = TypeVar('TConfig', bound=BaseModel)
TUpdate = TypeVar('TUpdate', bound=BasePayload)


class ReadUpdateEndpoint(Endpoint, Generic[TConfig, TUpdate]):
    """Shared implementation for read/update-only configuration endpoints."""

    endpoint_path: str
    config_response_model: type[TConfig]

    def get_config(self, item_id: str | int | None = None):
        endpoint = self._item_endpoint(item_id)
        data_model = (
            self.config_response_model
            if item_id is not None
            else list[self.config_response_model]
        )
        response = ApiResponse[data_model].model_validate(
            self._client._get(endpoint)
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)
        return response.data

    def update(self, payload: TUpdate) -> TConfig:
        item_id = getattr(payload, 'id', None)
        if item_id is None:
            raise ValueError(
                f'{self.__class__.__name__}.update() requires payload.id'
            )
        data = payload.asdict()
        data.pop('id', None)
        response = self._client._put_data(
            endpoint=self._item_endpoint(item_id),
            data_model=self.config_response_model,
            params=data,
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)
        return cast(TConfig, response.data)

    def update_bulk(self, payloads: list[TUpdate]) -> list[TConfig]:
        response = self._client._put(
            endpoint=self.endpoint_path,
            data_model=list[self.config_response_model],
            params={'data': [payload.asdict() for payload in payloads]},
        )
        if not response.success or response.data is None:
            raise TeltonikaApiException(response.errors)
        return cast(list[TConfig], response.data)

    def _item_endpoint(self, item_id: str | int | None) -> str:
        return (
            f'{self.endpoint_path}/{item_id}'
            if item_id is not None
            else self.endpoint_path
        )
