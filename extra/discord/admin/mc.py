from datetime import datetime
from pathlib import Path

import yaml
import discord
from discord import (
    ApplicationContext,
    Guild,
    Interaction,
    SelectOption,
    Member,
    Embed,
    ButtonStyle,
)
from discord.embeds import EmptyEmbed
from discord.ui import InputText, View, Modal, Select, Button, select, button

from plugins.discord.client import BaseCog, Bot

BC_PLUGIN_PATH = Path() / "../CT-BC"
BC_WHITELIST_CONFIG_PATH = BC_PLUGIN_PATH / "plugins" / "BungeeWhitelist" / "config.yml"


WARN_MESSAGE = """# 不廢話伺服器準則，請詳細察看

如無法加入者請至 <#1000064736928473168> 張貼錯誤訊息截圖會有專人為您服務 <:ctecskin1:1172165911172624464>

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


BASE_GUILD_ID = 933290709589577728  # 伺服器 ID
SMP_ROLE_ID = 1003709216000839761  # 生存服玩家/後勤
CMP_ROLE_ID = 1003649146244313189  # 創造服開發者
ARCHITECT_ROLE_ID = 1003649146244313189  # 建築組
FIRST_INSTANCE_ROLE_ID = 1000090304671666306  # 一審[通過表單等待審核]
SECOND_INSTANCE_ROLE_ID = 1049504039211118652  # 通過二審語音

# for-testing
# BASE_GUILD_ID = 803099240800714802  # 伺服器 ID
# SMP_ROLE_ID = 1196581001695084615  # 生存服玩家/後勤
# CMP_ROLE_ID = 1196581137288528054  # 創造服開發者
# ARCHITECT_ROLE_ID = 1196581195060879401  # 建築組
# FIRST_INSTANCE_ROLE_ID = 1196581237477879808  # 一審[通過表單等待審核]
# SECOND_INSTANCE_ROLE_ID = 1196581281585184768  # 通過二審語音

NAME_ROLES_ID_MAP = {
    "SMP": SMP_ROLE_ID,
    "CMP": CMP_ROLE_ID,
    "architect": ARCHITECT_ROLE_ID,
    "first_instance": FIRST_INSTANCE_ROLE_ID,
    "second_instance": SECOND_INSTANCE_ROLE_ID,
}


def add_whitelist(mc_id: str) -> bool:
    """添加白名單"""
    yaml_data = yaml.safe_load(BC_WHITELIST_CONFIG_PATH.read_text(encoding="utf-8"))
    whitelisted: list[str] = yaml_data["whitelist"]["global"]["whitelisted"]

    if mc_id not in set(whitelisted):
        whitelisted.append(mc_id)

        yaml.dump(
            yaml_data,
            BC_WHITELIST_CONFIG_PATH.open("w", encoding="utf-8"),
            allow_unicode=True,
        )
        return True
    return False


async def check_role(base_guild: Guild, ctx: ApplicationContext) -> bool:
    if member := await base_guild.fetch_member(ctx.author.id):
        roles = filter(
            # 1043786472207167558 =>> 審核身分組 ID
            #  933383039604637766 =>> admin 身分組 ID
            # (1043786472207167558, 933383039604637766)
            # For-test
            # (1196795438477623427, 1196795390914203690)
            lambda x: x.id in (1043786472207167558, 933383039604637766),
            member.roles,
        )
        if list(roles):
            return True
    await ctx.respond("你並非管理人員，無法使用此指令", ephemeral=True)
    return False


class MyView(View):
    def __init__(self, member: Member, bot: "Bot", base_guild: Guild) -> None:
        super().__init__(timeout=20)
        self.member = member
        self.bot = bot
        self.base_guild = base_guild

        def _map_from_options(*option: SelectOption) -> dict[str, SelectOption]:
            return {o.value: o for o in option}

        self.role_options: dict[str, SelectOption] = _map_from_options(
            SelectOption(label="生存服玩家/後勤", value="SMP"),
            SelectOption(label="創造服開發者", value="CMP"),
            SelectOption(label="建築組", value="architect"),
        )
        self.instances_options = _map_from_options(
            SelectOption(label="一審", value="first_instance"),
            SelectOption(label="二審", value="second_instance"),
        )

        roles_id = [role.id for role in member.roles]
        if SMP_ROLE_ID in roles_id:
            self.role_options["SMP"].default = True
        if CMP_ROLE_ID in roles_id:
            self.role_options["CMP"].default = True
        if ARCHITECT_ROLE_ID in roles_id:
            self.role_options["architect"].default = True

        if FIRST_INSTANCE_ROLE_ID in roles_id:
            self.instances_options["first_instance"].default = True
        if SECOND_INSTANCE_ROLE_ID in roles_id:
            self.instances_options["second_instance"].default = True

        select_role: Select = self.get_item("add_member:select_role")
        select_role.options.extend(self.role_options.values())
        select_role.max_values = len(select_role.options)

        select_status: Select = self.get_item("add_member:select_status")
        select_status.options.extend(self.instances_options.values())

    def _change_default(self, ids: list[str], data: dict[str, SelectOption]) -> None:
        for option in data.values():
            option.default = option.value in ids

    async def update_user(self) -> None:
        member = await self.base_guild.fetch_member(self.member.id)
        roles_id = [role.id for role in member.roles]

        for id, option in {**self.role_options, **self.instances_options}.items():
            role_id = NAME_ROLES_ID_MAP[id]
            role = self.base_guild.get_role(role_id)

            if role is None:
                print(f"Role {id} not found")
                continue
            if option.default:
                if role_id not in roles_id:
                    print(f"add {role.name}")
                    await self.member.add_roles(role)
            elif role_id in roles_id:
                print(f"remove {role.name}")
                await self.member.remove_roles(role)

    @select(custom_id="add_member:select_role", placeholder="請選擇成員組別", min_values=0)
    async def select_role(self, select: Select, interaction: Interaction) -> None:
        self._change_default(select.values, self.role_options)
        await self.update_user()
        await interaction.response.edit_message(view=self)

    @select(custom_id="add_member:select_status", placeholder="請選擇成員狀態", min_values=0)
    async def select_status(self, select: Select, interaction: Interaction) -> None:
        self._change_default(select.values, self.instances_options)
        await self.update_user()
        await interaction.response.edit_message(view=self)

    @button(label="添加白名單", style=ButtonStyle.green, custom_id="add_whitelist")
    async def add_whitelist(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_modal(WhitelistModal(self.base_guild))

    @button(
        label="預設[SMP&二審&發送DM]",
        style=ButtonStyle.primary,
        custom_id="base_second_instance",
    )
    async def base_second_instance(
        self,
        button: Button,
        interaction: Interaction,
    ) -> None:
        self.role_options["SMP"].default = True
        self.instances_options["first_instance"].default = False
        self.instances_options["second_instance"].default = True
        await self.update_user()

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
            icon_url=icon.url if (icon := self.base_guild.icon) else EmptyEmbed,
        )
        await self.member.send(WARN_MESSAGE, embed=embed)

        await interaction.response.send_modal(WhitelistModal(self.base_guild))
        await self.on_timeout()

    async def on_timeout(self) -> None:
        self.disable_all_items()
        await self.message.edit(view=self)


class WhitelistModal(Modal):
    def __init__(self, base_guild: Guild) -> None:
        super().__init__(
            InputText(
                label="Minecraft ID",
                custom_id="minecraft_id",
                placeholder="Minecraft ID",
            ),
            title="添加白名單",
        )
        self.base_guild = base_guild

    async def callback(self, interaction: Interaction) -> None:
        minecraft_id = self.children[0].value
        add_whitelist(minecraft_id)

        embed = Embed(
            description="用戶添加完畢",
            color=discord.Color.random(),
        )
        embed.add_field(name="Minecraft ID", value=minecraft_id)

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


class MinecraftCog(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.base_guild = self.bot.get_guild(BASE_GUILD_ID)

    @discord.slash_command(guild_only=True, name="移除雲鎮白名單")
    @discord.option("mc_id", str)
    async def del_whitelist(
        self,
        ctx: ApplicationContext,
        mc_id: str,
    ):
        if not await check_role(ctx):
            return

        # 移除白名單
        yaml_data = yaml.safe_load(BC_WHITELIST_CONFIG_PATH.read_text(encoding="utf-8"))
        whitelisted: list[str] = yaml_data["whitelist"]["global"]["whitelisted"]

        if mc_id in set(whitelisted):
            whitelisted.remove(mc_id)

            yaml.dump(
                yaml_data,
                BC_WHITELIST_CONFIG_PATH.open("w", encoding="utf-8"),
                allow_unicode=True,
            )
            await ctx.send(f"{mc_id} 以從白名單內移除")
        else:
            await ctx.send(f"{mc_id} 不在白名單內")

    @discord.user_command(name="添加成員")
    async def add_member(self, ctx: ApplicationContext, member: Member) -> None:
        await self.add_member_command(ctx, member)

    @discord.slash_command(name="添加白名單")
    async def add_whitelist(self, ctx: ApplicationContext) -> None:
        if not await check_role(self.base_guild, ctx):
            return

        await ctx.response.send_modal(WhitelistModal(self.base_guild))

    @discord.slash_command(guild_only=True, name="添加成員")
    async def add_member_command(
        self,
        ctx: ApplicationContext,
        member: Member,
    ) -> None:
        if not await check_role(self.base_guild, ctx):
            return

        await ctx.response.send_message(
            view=MyView(member, self.bot, self.base_guild),
            ephemeral=True,
        )

    async def cog_before_invoke(self, ctx: ApplicationContext) -> None:
        if not self.base_guild:
            self.base_guild = await self.bot.fetch_guild(BASE_GUILD_ID)


def setup(bot: "Bot"):
    bot.add_cog(MinecraftCog(bot))
