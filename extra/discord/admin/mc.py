import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Literal, Optional, TypedDict, Union, overload

import discord
import requests
import ruamel.yaml
from discord import ApplicationContext, Embed, Guild, Member
from discord.embeds import EmptyEmbed
from discord.utils import basic_autocomplete

from plugins.discord.client import BaseCog, Bot

PANEL_API_URL = os.getenv("PANEL_API_URL")
PANEL_ADMIN_TOKEN = os.getenv("PANEL_ADMIN_TOKEN")

INSTANCE_CONFIG_PATH = Path("instance_config.json")
BC_PLUGIN_PATH = Path() / "../CT-BC" / "plugins"
BC_WHITELIST_CONFIG_PATH = BC_PLUGIN_PATH / "BungeeCordWhitelistCT" / "config.yml"
# BC_PLUGIN_PATH = Path() / "../CT-BC"
# BC_WHITELIST_CONFIG_PATH = BC_PLUGIN_PATH / "plugins" / "BungeeWhitelist"
#  / "config.yml"
yaml = ruamel.yaml.YAML()


WARN_MESSAGE = """# 不廢話伺服器準則，請詳細察看

如無法加入者請至 <#1000064736928473168> 張貼錯誤訊息截圖會有專人為您服務 <:ctecskin1:1172165911172624464>

## 伺服器資訊

- 伺服器 IP 請至 <#1112749547412787280> 查看
- 伺服器指令請至 <#1112752011557994617> 查看
- 伺服器有一些自訂合成，請至 <#1112752011557994617> 查看
- 伺服器種子碼: `-8180004378910677489`
- 伺服器版本: `1.17.1`
- 跨版本支持: `1.12.2~1.20.1` 皆可加入

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

SMP_ROLE_ID = 1138650736872399008  # 生存服玩家/後勤
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
    "first_instance": FIRST_INSTANCE_ROLE_ID,
    "second_instance": SECOND_INSTANCE_ROLE_ID,
}

ANSI_ESCAPE = re.compile(r"(\x08|\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")
MINECRAFT_LIST_PATTERN = re.compile(
    r"^\[Server\] \[(\d{2}:\d{2}:\d{2})(?: [^\]]*)?\](?: \[[^\]]*/INFO\])?: "
    r"(?:There are (\d+) of a max of (\d+) players online|Players online (\d+)/(\d+))(?:\: \[(.*?)\])?"
)


class WhitelistData(TypedDict):
    groups: dict[str, list[str]]
    whitelist: dict[str, list[str]]
    specialWhitelist: dict[str, list[str]]


@dataclass
class ServerInfo:
    online_count: int
    max_count: int
    players: list[str]


@dataclass
class InstanceInfo:
    uuid: str
    daemonId: str


def call_api(method: Literal["GET", "POST"], endpoint: str, **kwargs) -> Optional[Any]:
    headers = kwargs.pop("headers", {})
    return (
        requests.request(
            method,
            f"{PANEL_API_URL}{endpoint}",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "X-Requested-With": "XMLHttpRequest",
                **headers,
            },
            **kwargs,
            timeout=10,
        )
        .json()
        .get("data", None)
    )


def parse_online_players(log_output: str) -> Optional[tuple[ServerInfo, datetime]]:
    log_output = ANSI_ESCAPE.sub("", log_output)
    lines = log_output.splitlines()

    for line in lines:
        if match := MINECRAFT_LIST_PATTERN.match(line.strip().removeprefix(">").strip()):
            log_time = datetime.strptime(match.group(1), "%H:%M:%S")
            online_count = int(match.group(2) or match.group(4))
            max_count = int(match.group(3) or match.group(5))
            player_str = match.group(6)
            players = [p.strip() for p in re.split(r"[,\s]+", player_str) if p] if player_str else []

            return ServerInfo(online_count=online_count, max_count=max_count, players=players), log_time

    return None


def get_instance_status(uuid: str, daemonId: str) -> Optional[int]:
    """
    -1: 忙碌
     0: 關閉
     1: 關閉中
     2: 啟動中
     3: 運行中
    """
    params = {"apikey": PANEL_ADMIN_TOKEN, "uuid": uuid, "daemonId": daemonId}

    status_out = call_api("GET", "/api/instance", params=params)
    if status_out is None:
        return None

    return status_out.get("status", None)


async def check_server_alive(uuid: str, daemonId: str) -> tuple[bool, Optional[ServerInfo]]:
    params = {"apikey": PANEL_ADMIN_TOKEN, "uuid": uuid, "daemonId": daemonId}

    if (status := get_instance_status(uuid, daemonId)) is None or status != 3:
        return False, None

    old_log_output = call_api("GET", "/api/protected_instance/outputlog", params={**params, "size": 800})
    old_result = parse_online_players(old_log_output)
    start_time = datetime.now()
    if not call_api("POST", "/api/protected_instance/command", params={**params, "command": "list"}):
        print("Failed to send command")
        return False, None

    if datetime.now() - start_time < timedelta(seconds=1):
        await asyncio.sleep(1)

    for _ in range(5):
        log_output = call_api("GET", "/api/protected_instance/outputlog", params={**params, "size": 800})
        result = parse_online_players(log_output)
        if result:
            info, log_time = result
            if not old_result or info != old_result[0] or log_time - old_result[1] > timedelta(seconds=1):
                return True, info
        await asyncio.sleep(1)

    print("Failed to parse server info after 5 attempts")
    return False, None


@overload
def read_instance_config(name: None = ...) -> Dict[str, InstanceInfo]: ...
@overload
def read_instance_config(name: str = ...) -> Optional[InstanceInfo]: ...


def read_instance_config(
    name: Optional[str] = None,
) -> Union[Optional[InstanceInfo], Dict[str, InstanceInfo]]:
    try:
        if instance := json.loads(INSTANCE_CONFIG_PATH.read_text(encoding="utf-8")):
            if name is not None:
                return InstanceInfo(uuid=instance[name]["uuid"], daemonId=instance[name]["daemonId"])

            return {
                k: InstanceInfo(uuid=v["uuid"], daemonId=v["daemonId"])
                for k, v in instance.items()
                if isinstance(v, dict) and "uuid" in v and "daemonId" in v
            }
    except Exception:
        pass

    return None if name is not None else {}


def read_whitelist_file() -> WhitelistData:
    return yaml.load(BC_WHITELIST_CONFIG_PATH.read_text(encoding="utf-8"))


def add_whitelist(mc_id: str, group_name: str = "trial") -> bool:
    """添加白名單"""
    yaml_data = read_whitelist_file()
    whitelisted = yaml_data["whitelist"][group_name]

    if mc_id not in set(whitelisted):
        whitelisted.append(mc_id)

        yaml.dump(yaml_data, BC_WHITELIST_CONFIG_PATH.open("w", encoding="utf-8"))
        return True
    return False


async def get_whitelist_groups(_ctx: discord.AutocompleteContext):
    yaml_data = read_whitelist_file()
    return yaml_data["groups"].keys()


async def get_instance_ids(_ctx: discord.AutocompleteContext):
    return read_instance_config().keys()


async def check_role(base_guild: Guild, ctx: ApplicationContext, root_admin: bool = False) -> bool:
    # 1043786472207167558 =>> 審核身分組 ID
    roles = {1043786472207167558}
    if root_admin:
        #  933383039604637766 =>> admin 身分組 ID
        roles.add(933383039604637766)
    if member := await base_guild.fetch_member(ctx.author.id):
        if list(filter(lambda x: x.id in roles, member.roles)):
            return True
    await ctx.respond("你並非管理人員，無法使用此指令", ephemeral=True)
    return False


class MinecraftCog(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.log.info(f"BC Plugins Path {BC_PLUGIN_PATH.absolute()}")
        self.base_guild = self.bot.get_guild(BASE_GUILD_ID)

    @discord.slash_command(guild_only=True, name="移除雲鎮白名單")
    @discord.option("mc_id", str)
    @discord.option(
        "group",
        str,
        default="trial",
        autocomplete=basic_autocomplete(get_whitelist_groups),
    )
    async def del_whitelist(self, ctx: ApplicationContext, mc_id: str, group: str):
        if not await check_role(self.base_guild, ctx):
            return

        # 移除白名單
        yaml_data = yaml.load(BC_WHITELIST_CONFIG_PATH.read_text(encoding="utf-8"))
        whitelisted: list[str] = yaml_data["whitelist"][group]

        if mc_id in set(whitelisted):
            whitelisted.remove(mc_id)

            yaml.dump(yaml_data, BC_WHITELIST_CONFIG_PATH.open("w", encoding="utf-8"))
            self.log.info(f"{ctx.author.name} del_whitelist -> {mc_id}")
            await ctx.response.send_message(f"{mc_id} 以從白名單內移除", ephemeral=True)
        else:
            self.log.info(f"{ctx.author.name} try del_whitelist but user not in whitelist" f" -> {mc_id}")
            await ctx.response.send_message(f"{mc_id} 不在白名單內", ephemeral=True)

    @discord.slash_command(guild_only=True, name="伺服器當機重啟")
    @discord.option(
        "instance_name",
        str,
        autocomplete=basic_autocomplete(get_instance_ids),
    )
    async def dead_reboot(self, ctx: ApplicationContext, instance_name: str):
        roles = {SMP_ROLE_ID, CMP_ROLE_ID, ARCHITECT_ROLE_ID, SECOND_INSTANCE_ROLE_ID}
        if member := await self.base_guild.fetch_member(ctx.author.id):
            if not list(filter(lambda x: x.id in roles, member.roles)):
                await ctx.respond("你並非相關人員，無法使用此指令，若覺得有誤，請聯繫管理員", ephemeral=True)
                return

        await ctx.send_response(f"正在確認 {instance_name} 服務器狀態")

        config = read_instance_config(instance_name)
        if not config:
            self.log.info(f"{ctx.author.name} dead_reboot[找不到服務器] -> {instance_name}")
            await ctx.edit(content=f"找不到服務器 {instance_name}")
            return

        alive, _ = await check_server_alive(config.uuid, config.daemonId)
        if not alive:
            self.log.info(f"{ctx.author.name} dead_reboot -> {instance_name}")
            await ctx.edit(content=f"服務器 {instance_name} 當機中，正在重啟")

            params = {"apikey": PANEL_ADMIN_TOKEN, "uuid": config.uuid, "daemonId": config.daemonId}
            call_api("GET", "/api/protected_instance/kill", params=params)
            for _ in range(10):
                alive = get_instance_status(config.uuid, config.daemonId)
                if alive == 0:
                    break
                await asyncio.sleep(1)
            else:
                self.log.info(f"{ctx.author.name} dead_reboot[重啟失敗] -> {instance_name}")
                await ctx.edit(content=f"服務器 {instance_name} 重啟失敗")
                return

            call_api("GET", "/api/protected_instance/open", params=params)
            await ctx.edit(content=f"服務器 {instance_name} 啟動中")

            for _ in range(10):
                await asyncio.sleep(1)
                alive = get_instance_status(config.uuid, config.daemonId)
                if alive == 3:
                    break
            else:
                self.log.info(f"{ctx.author.name} dead_reboot[重啟失敗] -> {instance_name}")
                await ctx.edit(content=f"服務器 {instance_name} 重啟失敗")
                return

            self.log.info(f"{ctx.author.name} dead_reboot[重啟成功] -> {instance_name}")
            await ctx.edit(content=f"服務器 {instance_name} 重啟成功")
            return

        await ctx.edit(content=f"服務器 {instance_name} 正常運行中，無需重啟")

    @discord.slash_command(name="添加白名單")
    @discord.option("mc_id", str, required=True)
    @discord.option(
        "group",
        str,
        default="trial",
        autocomplete=basic_autocomplete(get_whitelist_groups),
    )
    async def add_whitelist(self, ctx: ApplicationContext, mc_id: str, group: str) -> None:
        # 檢查權限，如果 trial 則可由審核人員執行
        # 若為非 trial 則需為管理人員
        if not await check_role(self.base_guild, ctx, root_admin=group != "trial"):
            return

        if add_whitelist(mc_id, group_name=group):
            self.log.info(f"{ctx.author.name} add_whitelist -> {mc_id}")
            await ctx.response.send_message(f"已將 {mc_id} 加入白名單 [{group}]", ephemeral=True)
        else:
            self.log.info(f"{ctx.author.name} try add_whitelist but user already in whitelist -> {mc_id}")
            await ctx.response.send_message(f"{mc_id} 已經於加入白名單內", ephemeral=True)

    @discord.user_command(name="添加一審成員")
    @discord.option("user", Member)
    async def add_first_role(self, ctx: ApplicationContext, user: Member) -> None:
        if not await check_role(self.base_guild, ctx):
            return

        if FIRST_INSTANCE_ROLE_ID in map(lambda x: x.id, user.roles):
            self.log.info(f"{ctx.author.name} add_first_role[添加無效] -> {user.name}")
            await ctx.response.send_message(f"{user.name} 已經是一審成員", ephemeral=True)
        else:
            self.log.info(f"{ctx.author.name} add_first_role -> {user.name}")
            await user.add_roles(self.base_guild.get_role(FIRST_INSTANCE_ROLE_ID))
            await ctx.response.send_message(f"已將 {user.name} 加入一審成員", ephemeral=True)

    @discord.user_command(name="添加二審成員")
    @discord.option("user", Member)
    async def add_second_role(self, ctx: ApplicationContext, user: Member) -> None:
        if not await check_role(self.base_guild, ctx):
            return

        role_ids = list(map(lambda x: x.id, user.roles))

        # Remove 一審成員 role
        if FIRST_INSTANCE_ROLE_ID in role_ids:
            await user.remove_roles(self.base_guild.get_role(FIRST_INSTANCE_ROLE_ID))

        if SECOND_INSTANCE_ROLE_ID in role_ids:
            self.log.info(f"{ctx.author.name} add_second_role[添加無效] -> {user.name}")
            await ctx.response.send_message(f"{user.name} 已經是二審成員", ephemeral=True)
        else:
            self.log.info(f"{ctx.author.name} add_second_role -> {user.name}")

            # Add 二審成員 role
            await user.add_roles(self.base_guild.get_role(SECOND_INSTANCE_ROLE_ID))

            # 發送加入訊息
            await self.send_join_message(user)
            await ctx.response.send_message(f"已將 {user.name} 加入二審成員", ephemeral=True)

    async def send_join_message(self, member: Member):
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
        await member.send(WARN_MESSAGE, embed=embed)

    async def cog_before_invoke(self, _ctx: ApplicationContext) -> None:
        if not self.base_guild:
            self.base_guild = await self.bot.fetch_guild(BASE_GUILD_ID)


def setup(bot: "Bot"):
    bot.add_cog(MinecraftCog(bot))
