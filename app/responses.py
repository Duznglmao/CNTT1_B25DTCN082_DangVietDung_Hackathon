from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    statusCode: int
    error: str | None = None
    message: str
    data: T | None
