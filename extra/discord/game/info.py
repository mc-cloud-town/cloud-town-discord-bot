import os
from dataclasses import dataclass


from discord import Embed
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
                d["metric"]["type"]: float(d["value"]),
            }

        return {k: cls(k, v.get("tick"), v.get("mspt")) for k, v in result.items()}


class InfoCog(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super(bot)
        self.prometheus = PrometheusConnect(
            os.getenv("PROMETHEUS_URL", "http://127.0.0.1:9090")
        )

    @commands.command()
    async def info(self, ctx: Context):
        embed = Embed()
        for k, v in ServerInfo.from_data(self.prometheus).items():
            embed.add_field(
                name=k["metric"]["job"],
                value=f"TPS: {v.mspt:.2f}\nMSPT: {v.mspt:.2f}",
                inline=True,
            )

        await ctx.send(embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(InfoCog(bot))
