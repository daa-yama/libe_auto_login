from typing import Optional
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_manager import GetElement, ActionElement
import logging
import os
from dotenv import load_dotenv

class Flow:
    """フロー統括（print版）。Chromeは外部受領、__init__/flowのみ定義。loggerは今回未使用。"""

    def __init__(self, chrome: WebDriver, logger: Optional[logging.Logger] = None) -> None:
        
        self.chrome = chrome
        self.logger = logger  # 受け取るだけ（今回は未使用）
        self.ge = GetElement()
        self.ae = ActionElement()
        print("[Flow] 初期化: ge/ae を生成しました")
        
        self.login_url = os.getenv("LOGIN_URL")
        self.login_email = os.getenv("LOGIN_EMAIL")
        self.login_password = os.getenv("LOGIN_PASSWORD")

        # 足りない場合に備えて（任意）
        if not all([self.login_url, self.login_email, self.login_password]):
            print("[WARNING] .env の値が不足している可能性があります。")

    def flow(self) -> None:
        print("[Flow] フロー開始")
        
        self.chrome.get(self.login_url)
        
        email = self.ge.get_by_css(self.chrome, "input[type='text']")
        passwd = self.ge.get_by_css(self.chrome, "input[type='password']")
        login  = self.ge.get_by_css(self.chrome, "button[type='submit']")
# login ボタンは使わず Enter 送信に統一する例
# login  = self.ge.get_by_css(self.chrome, "button[type='submit']")

        self.ae.clear_and_send_keys(email,  self.login_email)
        self.ae.clear_and_send_keys(passwd, self.login_password)

        passwd.send_keys(Keys.ENTER)

        print("[Flow] フロー終了")

