import pyperclip


def replace_name(n):
    return n.replace(' ', ', ')

def split_many(names):
    return [replace_name(n) for n in names]
        

def split_single(name):
    return replace_name(name)

def copy_clipboard(s):
    pyperclip.copy(s)
    pyperclip.paste()


if __name__ == '__main__':
    name = "폐호흡 디톡스 알로에베라 액상 합성 60ml 3mg"
    result = split_single(name)
    copy_clipboard(result)

