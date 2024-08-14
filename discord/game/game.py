import random
import re

import discord
from discord import Message

from plugins.discord.client import BaseCog, Bot

IP_MESSAGE = [
    "https://media.discordapp.net/stickers/1172167390990188596.webp?size=240",
    "你猜阿 .w.",
    "172.16.20.1:25560",
    "10.16.19.2:25565",
    "127.0.0.1",
    "192.168.225.9",
    "localhost",
    "raspberrypi.local",
    "請詳閱公開說明書!! https://discord.com/channels/933290709589577728/1036481756846633020",
]


class GameCog(BaseCog):
    @discord.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if re.match(r"(?<![\d\w])ip", message.content):
            await message.channel.send(random.choice(IP_MESSAGE))


def setup(bot: "Bot"):
    bot.add_cog(GameCog(bot))
