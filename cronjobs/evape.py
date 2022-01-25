import requests
from dataclasses import dataclass
from dotenv import dotenv_values

config = dotenv_values(".env")
NUM_OF_USERS = 2


@dataclass
class UserDto:
    id: str
    pwd: str


def read_user_info():
    users = []
    for i in range(NUM_OF_USERS):
        users.append(UserDto(id=config.get(f"ID{i+1}"), pwd=config.get(f"PWD{i+1}")))
    return users


def create_session():
    return requests.session()


def login(session, user: UserDto):
    login_url = "https://evape.kr/bbs/login_check.php"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {"url": "https://evape.kr/", "mb_id": user.id, "mb_password": user.pwd}
    session.post(login_url, headers=headers, data=payload)
    return session


def get_cookies(session):
    return session.cookies


def logout(session):
    logout_url = "https://evape.kr/bbs/logout.php"
    session.get(logout_url)


def get_token(session):
    token_url = "https://evape.kr/bbs/write_token.php"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    payload = {"bo_table": "free"}
    r = session.post(token_url, headers=headers, data=payload).json()
    return r["token"]


def write_post(session, token):
    post_url = "https://evape.kr/bbs/write_update.php"
    headers = {
        "content-type": "multipart/form-data",
        "cookie": get_cookies(session),
        "Referer": "https://evape.kr/bbs/write.php?bo_table=free",
    }

    payload = {
        "token": token,
        "uid": "2022012515183931",
        "wr_subject": "가입 인사드립니당 ~ :)",
        "wr_content": "<p>형님들 안녕하세요 오지게 인사 먼저 박습니다.&nbsp;</p><p>모두 즐거운 베이핑 하시죠</p>",
    }
    r = session.post(post_url, headers=headers, data=payload)
    print(r.json())


def main():
    users = read_user_info()
    user = users[0]
    session = login(create_session(), user)
    token = get_token(session)
    session = write_post(session, token)
    logout(session)
