import contextlib
from typing import AsyncGenerator, Generic, Protocol, Self, TypeVar

T = TypeVar("T")


class UowProtocol(Generic[T], Protocol):  # type: ignore
    @contextlib.asynccontextmanager
    async def transaction(self: Self) -> AsyncGenerator[T, None]:
        yield T  # type: ignore
