from rich.console import Console
from functools import wraps
from rich.table import Table

console = Console()


def rich_print(data):
    console.print(data)


def show_locals(f):
    @wraps(f)
    def wrap(*args, **kw):
        result = f(*args, **kw)
        console.print("show locals()")
        console.print(locals())
        return result

    return wrap


def pipe(data, *funcs):
    for fn in funcs:
        data = fn(data)
    return data


def get_table(headers) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    for header in headers:
        table.add_column(header)
    return table
