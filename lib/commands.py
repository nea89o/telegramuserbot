import typing

import pyrogram
from pyrogram.api import types as tgtypes

from lib.common import CommonContext
from util import property_decorator

commands = {}


def get_all_commands():
    return commands.values()


class CommandContext(CommonContext):
    def __init__(self, client: pyrogram.Client, channel, args: typing.List[str], message: tgtypes.Message):
        super().__init__(client, channel, message)
        import re
        self.args = args
        self.rest_content = re.sub('^.*? ', '', message.message)



def register_command(func):
    if not is_command(func):
        return
    commands[get_command_name(func)] = func


def is_command(func):
    return hasattr(func, 'name') and func.name is not None


def get_command_name(func):
    return func.name


def get_command_description(func):
    return func.description


def get_command_by_name(command_name: str):
    return commands[command_name.lower()]


name = property_decorator('name')
description = property_decorator('description')
