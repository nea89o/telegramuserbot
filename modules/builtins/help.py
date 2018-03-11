from lib import CommandContext, get_all_commands, name, description, get_command_name, get_command_description


@name('help')
@description('lists all commands with their descriptions')
def help_command(ctx: CommandContext):
    resp = ""
    for command in get_all_commands():
        resp += '%s - %s\n' % (get_command_name(command), get_command_description(command))
    ctx.respond(resp)
