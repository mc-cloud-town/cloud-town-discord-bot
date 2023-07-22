from . import BaseServer, Context
from .utils import FileEncode
from asyncio import AbstractEventLoop

class Server(BaseServer):
    def __init__(self, loop: AbstractEventLoop | None = ...) -> None: ...
    async def on_ping(self, ctx: Context): ...
    async def on_connect(self, ctx: Context, auth): ...
    async def on_disconnect(self, ctx: Context): ...
    async def on_server_start(self, ctx: Context): ...
    async def on_server_startup(self, ctx: Context): ...
    async def on_server_stop(self, ctx: Context): ...
    async def on_player_chat(self, ctx: Context, player_name: str, content: str): ...
    async def on_player_joined(self, ctx: Context, player_name: str): ...
    async def on_player_left(self, ctx: Context, player_name: str): ...
    async def on_file_sync(self, ctx: Context, data: FileEncode): ...
