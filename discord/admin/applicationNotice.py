import discord
from discord import Message

from plugins.discord.client import BaseCog, Bot


class ApplicationNoticeCog(BaseCog):
    @discord.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.webhook_id != 1197528292970991688:
            return
        await message.add_reaction("⭕")
        await message.add_reaction("❌")


def setup(bot: "Bot"):
    bot.add_cog(ApplicationNoticeCog(bot))
