import json
import yaml
from _typeshed import Incomplete
from pathlib import Path
from typing import Any, Dict, Generic, Literal, NamedTuple, Optional, TypeVar, Union

_RT = TypeVar('_RT', bound=NamedTuple)
_T = TypeVar('_T')

class UserAuth(NamedTuple):
    password: str
    display_name: Optional[str]

class UserData(NamedTuple):
    name: str
    display_name: Optional[str]

class ConfigType(NamedTuple):
    stop_plugins: list[str]
    users: Dict[str, UserAuth]
    plugins_path: str
    port: str

class Config(Generic[_RT]):
    directory: Incomplete
    config_type: Incomplete
    filepath: Incomplete
    default_config: Incomplete
    def __init__(self, config_name: str, config_path: Union[str, Path, None] = ..., config_type: Union[Literal['json'], Literal['yaml']] = ..., default_config: Optional[_RT] = ...) -> None: ...
    def check_config(self, replay: bool = ...) -> None: ...
    def read_config(self) -> dict: ...
    def write(self, data: _RT) -> None: ...
    def get(self, key: str, default: Optional[_T] = ...) -> _T: ...
    def set(self, key: str, value: Any) -> None: ...
    def append(self, key: str, value: Any, *, only_one: bool = ...) -> None: ...
    def remove(self, key: str, value: Any) -> None: ...
