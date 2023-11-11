import random
import re

from discord import Message
import discord

from plugins.discord.client import BaseCog, Bot


IP_MESSAGE = [
    "https://media.discordapp.net/stickers/1172167390990188596.webp?size=240",
    "https://media.discordapp.net/attachments/1025379525535748160/1052222785734328320/-1.png",  # noqa
    "你猜阿 .w.",
    "192.168.20.1:25560",
    "192.168.20.1:25565",
    "192.168.18.1:25560",
    "172.16.20.1:25560",
    "10.16.19.2:25565",
]


class GameCog(BaseCog):
    @discord.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if re.match(r"(?<![\d\w])ip", message.content):
            await message.channel.send(random.choice(IP_MESSAGE))


def setup(bot: "Bot"):
    bot.add_cog(GameCog(bot))
