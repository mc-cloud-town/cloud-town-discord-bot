from datetime import datetime
from pathlib import Path

import discord
from discord import Embed, Member
import yaml

from bot import ApplicationContext, BaseCog, Bot, Translator, cog_i18n

_ = Translator(__name__)

BC_PLUGIN_PATH = Path() / "../CT-BC"
BC_WHITELIST_CONFIG_PATH = BC_PLUGIN_PATH / "plugins" / "BungeeWhitelist" / "config.yml"


@cog_i18n
class MinecraftCog(BaseCog, name="Minecraft admin"):
    @discord.slash_command(
        guild_only=True,
        i18n_name=_("add_member"),
        i18n_description=_("添加雲鎮二審成員 & 添加白名單"),
    )
    @discord.option(
        "user",
        Member,
        i18n_name=_("對應的 DC 成員"),
        i18n_description=_("對應的 DC 成員"),
    )
    @discord.option(
        "mc_id",
        str,
        i18n_name=_("Minecraft ID"),
        i18n_description=_("該用戶的 MC_ID"),
    )
    async def add_member(self, ctx: ApplicationContext, user: Member, mc_id: str):
        # 1043786472207167558 =>> 審核身分組 ID
        # 933383039604637766 =>> admin 身分組 ID
        if ctx.author.id in (1043786472207167558, 933383039604637766):
            await ctx.respond(ctx._("你並非審核人員，無法使用此指令"))
            return

        # 1049504039211118652 =>> 二審身分組 ID
        rule = ctx.guild.get_role(1049504039211118652)
        await ctx.author.add_roles(rule)

        # 添加白名單
        yaml_data = yaml.safe_load(BC_WHITELIST_CONFIG_PATH.read_text(encoding="utf-8"))
        whitelisted: list[str] = yaml_data["whitelist"]["global"]["whitelisted"]

        if mc_id not in set(whitelisted):
            whitelisted.append(mc_id)

            yaml.dump(
                yaml_data,
                BC_WHITELIST_CONFIG_PATH.open("w", encoding="utf-8"),
                allow_unicode=True,
            )

        await ctx.respond(
            embed=Embed(
                title=ctx._("身份組已添加完成"),
                description=ctx._("已將 {user.mention} 添加二審身份組\nMC_ID: {mc_id}").format(
                    user=user,
                    mc_id=mc_id,
                ),
                color=0x00FF00,
            ),
            # ephemeral=True,
        )

        # 1112748827099795577 =>> 伺服器資訊-server-info 頻道
        embed = Embed(
            title="雲鎮工藝成員通知 - CT Member Notifications",
            color=0x00FF00,
            description=(
                "恭喜你，你已獲得本伺服器二審身分，您當前已可進入伺服器遊玩\n請詳閱 <#1112748827099795577>\n\n"
                "Congratulations, you have obtained the second instance status "
                "of this server, you can currently enter the server to playnPlease "
                "read <#1112748827099795577> carefully"
            ),
            timestamp=datetime.now(),
        )
        embed.set_footer(
            text="雲鎮工藝 - CloudTown",
            icon_url=ctx.guild.icon,
        )
        await user.send(embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(MinecraftCog(bot))
