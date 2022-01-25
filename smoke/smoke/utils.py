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


def split(product_name="폐호흡 슈퍼쿨 스트로베리 프로스트 액상 합성 60ml 3mg"):
    import pyperclip

    def _replace_name(n):
        return n.replace(" ", ", ")

    def _split_many(names):
        return [_replace_name(n) for n in names]

    def _split_single(name):
        return _replace_name(name)

    def _copy_clipboard(s):
        pyperclip.copy(s)
        pyperclip.paste()

    result = _split_single(product_name)
    _copy_clipboard(result)
