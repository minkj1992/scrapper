from rich.console import Console
from functools import wraps

console = Console()


def print_locals():
    console.print("print locals()")
    console.print(locals())


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
