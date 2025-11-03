from typing import Optional
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_manager import GetElement, ActionElement
import logging

class Flow:
    """フロー統括（print版）。Chromeは外部受領、__init__/flowのみ定義。loggerは今回未使用。"""

    def __init__(self, chrome: WebDriver, logger: Optional[logging.Logger] = None) -> None:
        self.chrome = chrome
        self.logger = logger  # 受け取るだけ（今回は未使用）
        self.ge = GetElement()
        self.ae = ActionElement()
        print("[Flow] 初期化: ge/ae を生成しました")

    def flow(self) -> None:
        print("[Flow] フロー開始")
        self.chrome.get("https://libecity.com/signin")

        email = self.ge.get_by_css(self.chrome, "input[type='text']")
        passwd = self.ge.get_by_css(self.chrome, "input[type='password']")
        login  = self.ge.get_by_css(self.chrome, "button[type='submit']")

        self.ae.clear_and_send_keys(email,  "test@example.com")
        self.ae.clear_and_send_keys(passwd, "test1234")

        passwd.send_keys(Keys.ENTER)

        print("[Flow] フロー終了")

