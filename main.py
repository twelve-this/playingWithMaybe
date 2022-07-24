from typing import Any, Callable, Union

MaybeFunction = Union[Callable, None]


class Maybe:
    def __init__(self, value: Any, *, allow_none: bool = False) -> None:
        self.value: Any = value
        self.allow_none: bool = allow_none
        self.function: MaybeFunction | None = None
        self.args: Any | None = None
        self.kwargs: Any | None = None
        self.function_name: str | None = None
        self.result: Maybe | None = None

    @classmethod
    def wrap(cls, value: Any, *, allow_none: bool) -> "Maybe":
        return cls(value=value, allow_none=allow_none)

    def then(self, function: MaybeFunction, *args: Any, **kwargs: Any) -> "Maybe":

        self._collect_function_data(function, args, kwargs)

        if self.allow_none and self.value is None:
            self._log_if_none()
            return self

        self._log_before_function_call()

        function_result = self.function(self.value, *self.args, **self.kwargs)

        self.result = (
            function_result
            if isinstance(function_result, Maybe)
            else Maybe.wrap(value=function_result, allow_none=self.allow_none)
        )

        self._log_after_function_call()
        self._raise_error_if_result_is_none()
        return self.result

    def _collect_function_data(
        self, function: MaybeFunction, args: tuple[Any], kwargs: dict[str, Any]
    ) -> None:
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.function_name = function.__name__

    def _raise_error_if_result_is_none(self) -> None:
        if not self.allow_none and self.result.value is None:
            raise ValueError(
                f"Using function '{self.function_name}': Value cannot be none"
            )

    def _log_before_function_call(self) -> None:
        m = f"Then function '{self.function_name}' applying to value {self.value} - with args {self.args} and with kwargs {self.kwargs}"
        print(m)

    def _log_after_function_call(self) -> None:
        m = f"Function {self.function_name} has result: {self.result.value}"
        print(m)
        print()

    def _log_if_none(self) -> None:
        m = f"None value is allowed and value is none. Function {self.function_name} with args {self.args} and {self.kwargs} is not called and none is returned instead"
        print(m)


def multiply_4(n):
    """Multiply by 4"""
    return n * 4


def add_5(n):
    return n + 5


def subtract_10(n):
    return n - 10


def add_2(n, *args, **kwargs):
    return n + 2


def subtract_18(n):
    return n - 18


def main():
    result = (
        Maybe(9)
        .then(multiply_4)
        .then(add_5)
        .then(subtract_10)
        .then(add_2, 5, 2, 523, a=5, b=11, c=456)
        .then(subtract_18)
    )
    print(result.value)


if __name__ == "__main__":
    main()
