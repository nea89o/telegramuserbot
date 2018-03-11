import ast

from lib import *


@name('eval')
@description('evals a given piece of python code')
def eval_command(ctx: CommandContext):
    ctx.edit("```\n%s\n```" % ctx.rest_content)
    try:
        block = ast.parse(ctx.rest_content, mode='exec')
        last = ast.Expression(block.body.pop().value)
    except KeyboardInterrupt:
        raise
    except SystemExit:
        raise
    except BaseException as e:
        ctx.respond("Compilation failed: %r" % e)
        return

    _globals, _locals = {}, {
        'ctx': ctx,
        'message': ctx.message,
        'client': ctx.client,
        'print':
            lambda *content, stdout=False:
            print(*content)
            if stdout
            else ctx.respond('\t'.join(map(str, content)))
    }
    try:
        exec(compile(block, '<string>', mode='exec'), _globals, _locals)
    except KeyboardInterrupt:
        raise
    except SystemExit:
        raise
    except BaseException as e:
        ctx.respond("Evaluation failed: %r" % str(e))
        return

    try:
        compiled = compile(last, '<string>', mode='eval')
    except KeyboardInterrupt:
        raise
    except SystemExit:
        raise
    except BaseException as e:
        ctx.respond("Last statement has to be an expression: %r" % str(e))
        return

    try:
        result = eval(compiled, _globals, _locals)
    except KeyboardInterrupt:
        raise
    except SystemExit:
        raise
    except BaseException as e:
        ctx.respond("Evaluation failed: %r" % str(e))
        return

    ctx.respond("Evaluation succes: \n```\n%s\n```" % str(result))
