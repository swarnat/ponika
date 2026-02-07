from dataclasses import asdict, dataclass
from enum import Enum
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar

if TYPE_CHECKING:
    from ponika import PonikaClient

from pydantic import BaseModel


T = TypeVar("T")


    
class TeltonikaApiError(BaseModel):
    """Custom exception for Teltonika API errors."""

    code: int
    error: str
    source: str
    section: Optional[str] = None

    def __str__(self) -> str:
        return f"Error {self.code}: {self.error} ({self.source}, {self.section})"


class Endpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self._client: "PonikaClient" = client    

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: None | T = None
    errors: Optional[List[TeltonikaApiError]] = None

@dataclass
class BasePayload:
    def asdict(self) -> dict:
        def convert(value):
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, list):
                return [convert(v) for v in value]
            if isinstance(value, bool):
                return "1" if value == True else "0"
            if isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            
            return value

        return convert(asdict(self))    
    
class Token(BaseModel):
    """Data model for token storage."""

    token: str
    expires_at: int
