from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...


OrderedT = TypeVar("OrderedT", bound=Ordered)
