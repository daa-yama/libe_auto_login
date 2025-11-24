import time
import logging
from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from simple_logger import SimpleLogger


class GetElement:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def _find(self, chrome: WebDriver, by: str, value: str) -> WebElement:
        try:
            self.logger.debug(f"[DEBUG] 要素取得開始\nBy={by}\nValue={value}")
            elem = chrome.find_element(by, value)
            self.logger.debug(f"[DEBUG] 要素取得完了\nBy={by}\nValue={value}")
            return elem

        except NoSuchElementException as e:
            self.logger.error(
                f"[ERROR] 要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}"
            )
            raise

        except Exception as e:
            self.logger.error(
                f"[ERROR] 想定外、要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}"
            )
            raise

    def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.ID, value)
        return elem

    def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.NAME, value)
        return elem

    def get_by_css(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.CSS_SELECTOR, value)
        return elem

    def get_by_xpath(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.XPATH, value)
        return elem

    def get_by_class_name(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.CLASS_NAME, value)
        return elem

    def get_by_tag_name(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.TAG_NAME, value)
        return elem

    def get_by_link_text(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.LINK_TEXT, value)
        return elem

    def get_by_partial_link_text(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.PARTIAL_LINK_TEXT, value)
        return elem


class ActionElement:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def send_keys(self, element: WebElement, text: str) -> None:
        """単純な入力用（クリアしない）"""
        try:
            self.logger.info("入力開始")
            element.send_keys(text)

            # パスワード欄ならマスクしてログ出力
            if element.get_attribute("type") == "password":
                masked = "*" * len(text)
                self.logger.info(f"入力完了: {masked}")
            else:
                self.logger.info(f"入力完了: {text}")

        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise

    def click(self, element: WebElement) -> None:
        try:
            self.logger.info("クリック開始")
            element.click()
            self.logger.info("クリック完了")
        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise

    def clear_and_send_keys(self, element: WebElement, text: str) -> None:
        """一度クリアしてから入力する"""
        try:
            self.logger.info("入力クリア＆開始")
            element.clear()
            element.send_keys(text)

            # パスワード欄ならマスクしてログ出力
            if element.get_attribute("type") == "password":
                masked = "*" * len(text)
                self.logger.info(f"入力完了: {masked}")
            else:
                self.logger.info(f"入力完了: {text}")

        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise

    def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
        """通常クリックがダメなときに JS クリックにフォールバック"""
        self.logger.info("クリック開始")
        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            self.logger.error(
                f"通常クリック不可（エラー種別: {type(e).__name__}）→ JavaScriptクリックでフォールバック"
            )
            try:
                chrome.execute_script("arguments[0].click();", element)
            except Exception as js_e:
                self.logger.error(f"JavaScriptクリックも失敗: {js_e}")
                raise
        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise
        self.logger.info("クリック完了")


if __name__ == "__main__":
    load_dotenv()
    email = os.getenv("LOGIN_EMAIL")
    password = os.getenv("LOGIN_PASSWORD")

    test_logger = SimpleLogger(debugMode=True).get_logger()

    chrome: WebDriver = webdriver.Chrome()
    try:
        chrome.get("https://libecity.com/signin")

        ge = GetElement(test_logger)
        action = ActionElement(test_logger)

        id_input = ge.get_by_css(chrome, "input[type='text']")
        action.clear_and_send_keys(id_input, email)

        password_input = ge.get_by_css(chrome, "input[type='password']")
        action.clear_and_send_keys(password_input, password)

        login_btn = ge.get_by_xpath(
            chrome, "//button[contains(normalize-space(.), 'ログイン')]"
        )
        action.click(login_btn)

        time.sleep(3)
        test_logger.info(f"[TEST] current_url={chrome.current_url}")
    finally:
        chrome.quit()