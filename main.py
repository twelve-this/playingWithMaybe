from __future__ import annotations

from typing import Any, Callable

MaybeFunction = Callable[[Any | None], Any | None]


class Maybe:

    def __init__(self, value: Any, allow_none: bool = False) -> None:
        self.value: Any = value
        self.allow_none: bool = allow_none
        self.function: MaybeFunction | None = None
        self.result: Maybe | None = None

    @classmethod
    def unit(cls, value: Any) -> Maybe:
        return cls(value)

    def bind(self, function) -> Maybe:
        self.function = function

        # if self.value is None:
        #     return self

        self._log()
        result = self.function(self.value)
        self.result = result if isinstance(result, Maybe) else Maybe.unit(result)
        self._raise_error_if_result_is_none()
        return self.result

        #m = f"Produced result: {result}"
        # print("done")
        # if isinstance(result, Maybe):
        #     return result
        # else:
        #     return Maybe.unit(result)

    def _raise_error_if_result_is_none(self) -> None:
        if not self.allow_none and self.result.value is None:
            raise ValueError(f"Using function '{self.function.__name__}': Value cannot be none")

    def _log(self) -> None:
        m = f"Using function {self.function.__name__} with parameter {self.value}"
        print(m)

def g(n):
    """Multiply by 4"""
    return n * 4


def h(n):
    #return None
    return n + 5


def i(n):
    #return None
    return n - 10


def main():
    result = (
        Maybe(4)
        .bind(g)
        .bind(h)
        .bind(i)
    )
    print(result.value)


if __name__ == "__main__":
    main()
