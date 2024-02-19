from datetime import datetime
from datetime import timezone, timedelta

from discord import Color, Embed
from discord.ext import commands
from discord.ext.commands import Context

from plugins.discord.client import BaseCog, Bot


class TimeCog(BaseCog):
    @commands.command()
    async def time(self, ctx: Context):
        embed = Embed(color=Color.random(), timestamp=datetime.now())

        now = lambda x: datetime.now(tz=timezone(timedelta(hours=x))).strftime("%Y-%m-%d %H:%M:%S")
        embed.add_field(
            name="UTC+8 (台灣/中國/香港/澳洲西部)",
            value=now(8),
        )
        embed.add_field(
            name="UTC+12 (諾福克島夏令時間)",
            value=now(12),
        )
        embed.add_field(
            name="UTC-8 (溫哥華/美國太平洋-洛杉磯)",
            value=now(-8),
        )
        embed.add_field(name="UTC-6 (美國中部-芝加哥)", value=now(-6))
        embed.add_field(name="UTC-7 (美國山區-丹佛 & 鳳凰城)", value=now(-7))
        embed.add_field(name="UTC-8 (美國太平洋-洛杉磯)", value=now(-8))
        embed.add_field(name="UTC-9 (美國阿拉斯加-安克雷奇)", value=now(-9))
        embed.add_field(name="UTC-10 (美國夏威夷-檀香山)", value=now(-10))

        embed.set_footer(
            text="雲鎮工藝 - CloudTown",
            icon_url=ctx.guild.icon,
        )

        await ctx.send(embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(TimeCog(bot))
