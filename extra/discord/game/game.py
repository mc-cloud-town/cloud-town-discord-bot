import random

from discord import Cog, Message

from plugins.discord.client import BaseCog, Bot


IP_MESSAGE = [
    "https://cdn.discordapp.com/attachments/998231869969662052/1136471507250450442/2023-08-03_09-31-08.mp4",  # noqa
    "https://media.discordapp.net/attachments/1025379525535748160/1052222785734328320/-1.png",  # noqa
    "https://cdn.discordapp.com/attachments/998231869969662052/1136474709534445618/QDG8FY9Q83GUAFL9EJQ.png",  # noqa
]


class MinecraftCog(BaseCog):
    @Cog.listener
    async def on_message(self, message: Message) -> None:
        if "ip" in message.content:
            await message.channel.send(random.choice(IP_MESSAGE))


def setup(bot: "Bot"):
    bot.add_cog(MinecraftCog(bot))
