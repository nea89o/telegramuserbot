import pyrogram
from pyrogram.api import types as tgtypes


class CommonContext:
    def __init__(self, client: pyrogram.Client, channel, message: tgtypes.Message):
        self.client = client
        self.channel = channel
        self.message = message
        self.author = message.from_id

    def respond(self, text):
        self.client.send_message(self.channel, text=text)

    def edit(self, text):
        self.client.edit_message_text(chat_id=self.channel, message_id=self.message.id, text=text)
