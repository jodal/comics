from collections.abc import Callable, Iterable
from typing import Any, overload

type _Validators = Callable[[Any], object] | Iterable[Callable[[Any], object]]

class Env:
    def __init__(
        self,
        *,
        allowed_chars: Iterable[str] = ...,
        upper: bool = False,
    ) -> None: ...
    @staticmethod
    def read_env(path: str = ".env", override: bool = False) -> bool: ...
    @overload
    def str(self, name: str, *, validate: _Validators = ()) -> str: ...
    @overload
    def str(
        self,
        name: str,
        *,
        default: None,
        validate: _Validators = (),
    ) -> str | None: ...
    @overload
    def str(self, name: str, *, default: str, validate: _Validators = ()) -> str: ...
    @overload
    def int(self, name: str, *, validate: _Validators = ()) -> int: ...
    @overload
    def int(
        self,
        name: str,
        *,
        default: None,
        validate: _Validators = (),
    ) -> int | None: ...
    @overload
    def int(self, name: str, *, default: int, validate: _Validators = ()) -> int: ...
    @overload
    def bool(self, name: str, *, validate: _Validators = ()) -> bool: ...
    @overload
    def bool(
        self,
        name: str,
        *,
        default: None,
        validate: _Validators = (),
    ) -> bool | None: ...
    @overload
    def bool(self, name: str, *, default: bool, validate: _Validators = ()) -> bool: ...
    @overload
    def float(self, name: str, *, validate: _Validators = ()) -> float: ...
    @overload
    def float(
        self,
        name: str,
        *,
        default: None,
        validate: _Validators = (),
    ) -> float | None: ...
    @overload
    def float(
        self,
        name: str,
        *,
        default: float,
        validate: _Validators = (),
    ) -> float: ...
    @overload
    def list(self, name: str, *, validate: _Validators = ()) -> list[str]: ...
    @overload
    def list(
        self,
        name: str,
        *,
        default: None,
        validate: _Validators = (),
    ) -> list[str] | None: ...
    @overload
    def list(
        self,
        name: str,
        *,
        default: list[str],
        validate: _Validators = (),
    ) -> list[str]: ...
