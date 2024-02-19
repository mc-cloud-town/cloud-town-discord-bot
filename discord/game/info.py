import os
from datetime import datetime
from dataclasses import dataclass

from discord import Color, Embed
from discord.ext import commands
from discord.ext.commands import Context
from prometheus_api_client import PrometheusConnect

from plugins.discord.client import BaseCog, Bot


@dataclass
class ServerInfo:
    name: str
    tps: float
    mspt: float

    @classmethod
    def from_data(cls, prometheus: PrometheusConnect) -> dict[str, "ServerInfo"]:
        result: dict[str, dict] = {}

        data: list[dict] = prometheus.custom_query("minecraft_tick")
        for d in data:
            job = d["metric"]["job"]
            result[job] = {
                **result.get(job, {}),
                d["metric"]["type"]: float(d["value"][1]),
            }

        return {k: cls(k, v.get("tps"), v.get("mspt")) for k, v in result.items()}


class InfoCog(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        self.prometheus = PrometheusConnect(os.getenv("PROMETHEUS_URL", "http://127.0.0.1:9090"))

    @commands.command()
    async def info(self, ctx: Context):
        embed = Embed(color=Color.random(), timestamp=datetime.now())
        for k, v in ServerInfo.from_data(self.prometheus).items():
            embed.add_field(
                name=k,
                value=f"TPS: {v.tps:.2f}\nMSPT: {v.mspt:.2f}",
                inline=True,
            )

        embed.set_footer(
            text="雲鎮工藝 - CloudTown",
            icon_url=ctx.guild.icon,
        )

        await ctx.send(embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(InfoCog(bot))
