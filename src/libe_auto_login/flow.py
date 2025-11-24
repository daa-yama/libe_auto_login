import time
import logging
import os
from typing import Optional

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from dotenv import load_dotenv

from selenium_manager import GetElement, ActionElement
from simple_logger import SimpleLogger


class Flow:

    def __init__(self, chrome: WebDriver, logger: Optional[logging.Logger] = None) -> None:
        
        self.chrome = chrome
        if logger is None:
            from simple_logger import SimpleLogger
            self.logger = SimpleLogger(debugMode=True).get_logger()
        else:
            self.logger = logger
        self.ge = GetElement(self.logger)
        self.ae = ActionElement(self.logger)
        self.logger.info("[Flow] 初期化: ge/ae を生成しました")
        self.login_url = os.getenv("LOGIN_URL")
        self.login_email = os.getenv("LOGIN_EMAIL")
        self.login_password = os.getenv("LOGIN_PASSWORD")

        # 足りない場合に備えて（任意）
        if not all([self.login_url, self.login_email, self.login_password]):
            self.logger.warning("[WARNING] .env の値が不足している可能性があります。")

    def flow(self) -> None:
        self.logger.info("[Flow] フロー開始")
        
        self.chrome.get(self.login_url)
        
        email = self.ge.get_by_css(self.chrome, "input[type='text']")
        passwd = self.ge.get_by_css(self.chrome, "input[type='password']")
        login  = self.ge.get_by_css(self.chrome, "button[type='submit']")
# login ボタンは使わず Enter 送信に統一する例
# login  = self.ge.get_by_css(self.chrome, "button[type='submit']")

        self.ae.clear_and_send_keys(email,  self.login_email)
        self.ae.clear_and_send_keys(passwd, self.login_password)

        passwd.send_keys(Keys.ENTER)

        self.logger.info("[Flow] フロー終了")
        time.sleep(5)