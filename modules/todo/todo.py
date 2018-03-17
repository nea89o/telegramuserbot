import sqlite3

import lib


def init_todo_db(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
          id INTEGER PRIMARY KEY,
          text VARCHAR(1024)
        );
        """)
    conn.commit()


def add_todo(todo):
    conn = sqlite3.connect('todos.db')
    init_todo_db(conn)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO todos (text) VALUES (?);
        """, [todo])
    conn.commit()


def read_todos() -> sqlite3.Cursor:
    conn = sqlite3.connect('todos.db')
    init_todo_db(conn)
    c = conn.cursor()
    return c.execute(
        """
        SELECT id, text FROM todos LIMIT 50;
        """)


@lib.match_text('(?i)^TODO: (?P<todos>.*)$')
def handle_todo(ctx: lib.MatchContext):
    for todo in ctx.named_groups['todos'].split(','):
        todo = todo.strip()
        add_todo(todo)
        ctx.respond(todo + ' added')


@lib.name('todos')
def list_todos(ctx: lib.CommandContext):
    mes = 'Todos: \n'
    for row in read_todos():
        mes += '%d - %s\n' % row
    ctx.respond(mes)
