from _typeshed import Incomplete
from enum import Enum
from typing import Optional, Union

class ChatFormatting(Enum):
    OBFUSCATED: Incomplete
    BOLD: Incomplete
    STRIKETHROUGH: Incomplete
    UNDERLINE: Incomplete
    ITALIC: Incomplete
    BLACK: Incomplete
    DARK_BLUE: Incomplete
    DARK_GREEN: Incomplete
    DARK_AQUA: Incomplete
    DARK_RED: Incomplete
    DARK_PURPLE: Incomplete
    GOLD: Incomplete
    GRAY: Incomplete
    DARK_GRAY: Incomplete
    BLUE: Incomplete
    GREEN: Incomplete
    AQUA: Incomplete
    RED: Incomplete
    LIGHT_PURPLE: Incomplete
    YELLOW: Incomplete
    WHITE: Incomplete
    code: Incomplete
    mark: Incomplete
    color: Incomplete
    is_format: Incomplete
    is_color: Incomplete
    ansi: Incomplete
    def __init__(self, code: str, mark: Optional[str] = None, integer: Optional[int] = None, ansi: Optional[str] = None) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @classmethod
    def formats(cls): ...
    @classmethod
    def colors(cls): ...

mark_data: Incomplete

class FormatMessage:
    original_msgs: Incomplete
    def __init__(self, *msgs: Union[str, 'FormatMessage'], no_style: bool = False, no_mark: bool = False) -> None: ...
    def json(self): ...

def split_desc_text(msg: str) -> tuple[str, str]: ...
def get_ansi_console(msg: str) -> tuple[dict, str]: ...
def parse_style(desc: str) -> tuple[dict, str]: ...
