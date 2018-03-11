from typing import List

import pyrogram
from pyrogram.api import types as tgtypes


def property_decorator(key):
    def decorator(value):
        def wrapper(func):
            setattr(func, key, value)
            return func

        return wrapper

    return decorator


name = property_decorator('name')
description = property_decorator('description')


def is_command(func):
    return hasattr(func, 'name') and func.name is not None


def get_command_name(func):
    return func.name


def get_command_description(func):
    return func.description


commands = {}


def get_all_commands():
    return commands.values()


class CommandContext(object):
    def __init__(self, client: pyrogram.Client, channel, args: List[str], message: tgtypes.Message):
        import re
        self.args = args
        self.client = client
        self.channel = channel
        self.message = message
        self.rest_content = re.sub('^.*? ', '', message.message)
        self.author = message.from_id

    def respond(self, text):
        self.client.send_message(self.channel, text=text)

    def edit(self, text):
        self.client.edit_message_text(chat_id=self.channel, message_id=self.message.id, text=text)


def register_command(func):
    if not is_command(func):
        return
    commands[get_command_name(func)] = func
