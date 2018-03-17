import pyrogram
from pyrogram.api import types as tgtypes

from lib.common import CommonContext


def match_text(regex):
    import re
    regex = re.compile(regex)

    def wrapper(func):
        func.regex = regex
        return func

    return wrapper


match_scripts = {}


def is_match_script(func):
    return hasattr(func, 'regex') and func.regex is not None


def get_match_script_matcher(func):
    return func.regex


def register_match_script(func):
    match_scripts[func.regex] = func


class MatchContext(CommonContext):
    def __init__(self, client: pyrogram.Client, channel, message: tgtypes.Message, match, groups, named_groups):
        super().__init__(client, channel, message)
        self.match = match
        self.groups = groups
        self.named_groups = named_groups


def get_match_scripts():
    return match_scripts
