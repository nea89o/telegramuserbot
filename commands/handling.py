import sys
import traceback

import importlib
import os
import pyrogram
import re
import types
from pyrogram.api import types as tgtypes

import lib

PREFIX = "!"


def load_module(module):
    functions = [module.__dict__.get(a) for a in dir(module)
                 if isinstance(module.__dict__.get(a), types.FunctionType)]
    for func in functions:
        if lib.is_command(func):
            lib.register_command(func)


def load_commands(folder='modules'):
    for dirname, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            filename: str
            if filename.endswith('.py'):
                filename = filename[:-3]
                pos = os.path.join(dirname, filename)
                module = importlib.import_module(pos.replace('/', '.'))
                load_module(module)


def handle_commands(client: pyrogram.Client, update, users, chats):
    if not (isinstance(update, tgtypes.UpdateNewMessage)
            or isinstance(update, tgtypes.UpdateNewChannelMessage)
            or isinstance(update, tgtypes.UpdateNewEncryptedMessage)):
        return
    update: tgtypes.UpdateNewMessage
    message: tgtypes.Message = update.message
    author_id = message.from_id
    if author_id != client.user_id:
        # do not react to other people
        return
    text: str = message.message
    if text[:len(PREFIX)] != PREFIX:
        return
    parts = re.split(r'\s+', text)
    if len(parts) < 1:
        return
    command = parts[0][1:]
    args = parts[1:]
    cmd_func = lib.commands[command.lower()]
    ctx = lib.CommandContext(client=client, channel=message.to_id, args=args, message=message)
    try:
        cmd_func(ctx)
    except KeyError:
        ctx.respond('unknown command')
    except Exception as e:
        ctx.respond("unknown exception during execution. Error will be DM'd" + str(e))
        print(traceback.format_exc(), file=sys.stderr)
