import pyperclip
name = "폐호흡 슈퍼쿨 스트로베리 프로스트 액상 합성 60ml 3mg"
def replace_name(n):
    return n.replace(' ', ', ')

def split_many(names):
    return [replace_name(n) for n in names]
        

def split_single(name):
    return replace_name(name)

def copy_clipboard(s):
    pyperclip.copy(s)
    pyperclip.paste()



result = split_single(name)
copy_clipboard(result)

