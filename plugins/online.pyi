from _typeshed import Incomplete
from server import BaseServer, Context, Plugin
from server.utils import Config
from typing import overload

minecraft_list_match: Incomplete
minecraft_GList_match: Incomplete

class OnlineConfig(Config):
    online_enabled: bool
    query_online_names: Incomplete
    bungeecord_list: Incomplete

class Online(Plugin, config=OnlineConfig):
    _glist_rcon_catch: Incomplete
    def __init__(self, server: BaseServer) -> None: ...
    @staticmethod
    def handle_minecraft(data: str) -> set[str]: ...
    @staticmethod
    def handle_bungee(data: str) -> dict[str, set[str]] | None: ...
    @overload
    async def query(self, *, order: bool = ...) -> list[tuple[Context, set[str]]]: ...
    @overload
    async def query(self, *, order: bool = ...) -> dict[Context, set[str]]: ...
    def on_unload(self) -> None: ...

def setup(server: BaseServer): ...
