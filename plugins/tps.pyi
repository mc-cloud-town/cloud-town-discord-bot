from _typeshed import Incomplete
from server import BaseServer, Plugin
from server.utils import Config

minecraft_list_match: Incomplete
minecraft_GList_match: Incomplete

class OnlineConfig(Config):
    online_enabled: bool
    query_online_names: Incomplete
    bungeecord_list: Incomplete

class Tps(Plugin, config=OnlineConfig):
    def __init__(self, server: BaseServer) -> None: ...

def setup(server: BaseServer): ...
