from datetime import datetime
from pathlib import Path

import discord
from discord import ApplicationContext, Embed, Member
import yaml

from plugins.discord.client import BaseCog, Bot

BC_PLUGIN_PATH = Path() / "../CT-BC"
BC_WHITELIST_CONFIG_PATH = BC_PLUGIN_PATH / "plugins" / "BungeeWhitelist" / "config.yml"


WARN_MESSAGE = """# 不廢話伺服器準則，請詳細察看

如無法加入者請至 <#1000064736928473168> 張貼錯誤訊息截圖會有專人為您服務 :emoji_15:

## 伺服器資訊

- 伺服器 IP 請至 <#1112749547412787280> 查看
- 伺服器指令請至 <#1112752011557994617> 查看
- 伺服器有一些自訂合成，請至 <#1112752011557994617> 查看
- 伺服器種子碼: `-8180004378910677489`
- 伺服器版本: `1.17.1`
- 跨版本支持: `1.8~1.20.x` 皆可加入

## :warning: 成員守則

以下為相關成員守則
除審核時口述之內容外
其餘請您詳細閱讀了解

請注意成員注意在外言行
成員言行將影響伺服器整體觀感
請將您的暱稱後面加上 `MC ID` 以便成員辨識
例: `雲鎮工藝(cloudtown)`

1. 伺服器並無嚴格限制成員行為，但請成員自律，嚴禁使用客戶端外掛，無消耗物品，複製，礦物透視，飛行等模組
2. 非必要請勿跑圖搜尋資源，相關物品已有替代方案，擅自跑圖將會造成備份時的困擾
3. 請多協助共同專案的研究與實裝，生存服進度也請協助推移
4. 若想在生存發展自己的領域時，請注意選址是否合適，是否影響到其他空置域或者交通，也請不要跑到數萬格外發展，如發展的佳，將列入伺服器景點中
5. 禁止未經同意外流想法或技術，若要外流請先詢問，因此情節嚴重，將會從重量刑
6. 允許理性的各種梗、討論與辯論，但不允許不尊重他人相關立場之言論，如果有人表示不適請停止(學術研究不在此限，那裡你想發啥就發啥，除了ㄌㄌ)。
7. 如對伺服器營運、管理或規劃等等有建議者，歡迎與相關人員討論，以上如經舉發者將視情節懲處，嚴重違規者將移除成員資格
8. 這裡免費提供成員交流學習生電技術，若成員長時間有以下行為，將移除雲鎮工藝成員資格
  - 未在頻道中參與討論
  - 伺服器長期未登錄
  - 與成員間互動性差
  - 未曾分享過相關內容
  **以下情況不在此限**
  - 受邀請加入者
  - 已在某領域有開發者
  - 已證明有一定程度技術者
  - 曾在伺服器有貢獻者(後勤/開發)

> **共產** **不白目** **大家和樂** **玩得開心** **多上線** **沒上掰**

### :warning: 注意，請看完上面的規定，如果你不同意，請不要加入，加入即代表你同意並詳細讀完以上規定
### :warning: 注意，請看完上面的規定，如果你不同意，請不要加入，加入即代表你同意並詳細讀完以上規定
### :warning: 注意，請看完上面的規定，如果你不同意，請不要加入，加入即代表你同意並詳細讀完以上規定"""


class MinecraftCog(BaseCog, name="Minecraft admin"):
    @discord.slash_command(
        guild_only=True,
        i18n_name="add_member",
        i18n_description="添加雲鎮二審成員 & 添加白名單",
    )
    @discord.option(
        "user",
        Member,
        i18n_name="對應的 DC 成員",
        i18n_description="對應的 DC 成員",
    )
    @discord.option(
        "mc_id",
        str,
        i18n_name="Minecraft ID",
        i18n_description="該用戶的 MC_ID",
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
        await user.send(WARN_MESSAGE, embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(MinecraftCog(bot))