from pyrogram import Client

from commands import handle_commands, load_modules, handle_match_scripts


def update_handler(client, update, users, chats):
    handle_commands(client, update, users, chats)
    handle_match_scripts(client, update, users, chats)


def main():
    load_modules()
    client = Client(session_name="userbot")
    client.set_update_handler(update_handler)
    client.start()
    client.idle()


if __name__ == '__main__':
    main()
