from dataclasses import dataclass
from selenium import webdriver
from dotenv import dotenv_values
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())
config = dotenv_values(".env")
NUM_OF_USERS = 2


@dataclass
class UserDto:
    id: str
    pwd: str


def open_browser(browser, url):
    browser.get(url)
    browser.implicitly_wait(1)


def read_user_info():
    users = []
    for i in range(NUM_OF_USERS):
        users.append(UserDto(id=config.get(f"ID{i+1}"), pwd=config.get(f"PWD{i+1}")))
    return users


def input_text(component, text: str):
    component.send_keys(text)


def login(browser, user: UserDto):
    login_id = browser.find_element_by_css_selector("#ol_id")
    input_text(login_id, user.id)

    login_pw = browser.find_element_by_css_selector("#ol_pw")
    input_text(login_pw, user.pwd)
    submit_btn = browser.find_element_by_css_selector("#ol_submit")
    submit_btn.click()


def click_yes_to_alert(browser):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    WebDriverWait(browser, 10).until(EC.alert_is_present())
    browser.switch_to.alert.accept()


def write_post(browser):
    post_url = "https://evape.kr/bbs/write.php?bo_table=free"
    browser.get(post_url)

    subject = browser.find_element_by_css_selector("#wr_subject")
    input_text(subject, "가입 인사 친절하게 박습니다.")  # TODO: okky title로 대체

    iframe = browser.find_element_by_xpath('//*[@id="fwrite"]/div[1]/table/tbody/tr[3]/td/iframe')
    browser.switch_to.frame(iframe)
    text_btn = browser.find_element_by_css_selector(
        "#smart_editor2_content > div.se2_conversion_mode > ul > li:nth-child(3) > button"
    )
    text_btn.click()
    click_yes_to_alert(browser)

    text = browser.find_element_by_css_selector(
        "#smart_editor2_content > div.se2_input_area.husky_seditor_editing_area_container > textarea.se2_input_syntax.se2_input_text"
    )
    input_text(text, "안녕하세요 인사 오지게\n박습니다 행님들 \n")  # TODO: okky post 대체
    browser.switch_to.default_content()
    submit_btn = browser.find_element_by_css_selector("#btn_submit")
    submit_btn.click()


def logout(browser):
    logout_url = "https://evape.kr/bbs/logout.php"
    browser.get(logout_url)


def main():
    open_browser(browser, url="https://evape.kr")
    users = read_user_info()
    for user in users:
        login(browser, user)
        write_post(browser)
        logout(browser)
    browser.close()


main()
