from typing import Union

import discord
from discord import ApplicationContext, Embed, Member, Message

from plugins.discord.client import BaseCog, Bot


class ClearCog(BaseCog):
    @discord.slash_command(
        guild_only=True,
        name="刪除",
        description="刪除一個訊息",
    )
    @discord.default_permissions(manage_messages=True)
    @discord.option("message_id", str)
    @discord.option("reason", str, default="")
    async def delete(self, ctx: ApplicationContext, message_id: str, reason: str):
        message: Message = await ctx.fetch_message(int(message_id))
        author = ctx.author

        await message.delete(reason=f"由 {ctx.author} 清除 - {reason}")

        embed = Embed(title="刪除完畢", description=reason)
        embed.set_author(
            name=author,
            icon_url=author.avatar.url if author.avatar.url else None,
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(
        guild_only=True,
        name="批量刪除",
        description="刪除大量訊息",
    )
    @discord.default_permissions(manage_messages=True)
    @discord.option("reason", str, default=None)
    @discord.option("member", Member, default=None)
    @discord.option("count", int, min_value=1, max_value=512)
    @discord.option("before", str, default=None)
    @discord.option("after", str, default=None)
    async def purge(
        self,
        ctx: ApplicationContext,
        count: int,
        reason: Union[str, None],
        member: Union[Member, None],
        before: Union[str, None],
        after: Union[str, None],
    ):
        reason = reason or "無原因"
        if before and after:
            embed = Embed(
                title="錯誤!",
                description="`before` 和 `after` 選項不得同時出現",
                color=0xE74C3C,
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        elif before:
            before: Message = await ctx.fetch_message(int(before))
        elif after:
            after: Message = await ctx.fetch_message(int(after))

        await ctx.channel.purge(
            limit=count,
            check=lambda msg: msg.author == member or not member,
            before=before,
            after=after,
            reason=f"由 {ctx.author} 清除 - 原因: {reason}",
        )
        embed = Embed(title="訊息刪除成功!", description=f"原因: {reason}")
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot: "Bot"):
    bot.add_cog(ClearCog(bot))
