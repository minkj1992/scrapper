import pyperclip
from spliter import split_single

def copy_clipboard(s):
    pyperclip.copy(s)
    pyperclip.paste()


if __name__ == '__main__':
    names = ["하이민트 히피 트레일", "로우민트 쿠쉬맨 망고 포도", "하이민트 아삽 그레이프", "로우민트 트랩퀸", "발린 블러디 베리", "하이민트 쿠쉬맨", "로우민트 쿠쉬맨", "발린 히피 트레일", "발린 패션 킬라", "로우민트 쿠쉬맨 망고 딸기", "로우민트 쿠쉬맨 망고 바나나"] 
    for name in names:
        nasty_fmt = f"폐호흡 네스티 {name}액상 합성 60ml"
        print(nasty_fmt)
        print(split_single(nasty_fmt))
        print()
    

