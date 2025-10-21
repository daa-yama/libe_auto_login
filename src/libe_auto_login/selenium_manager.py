from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException


class GetElement:
    def _find(self, chrome:WebDriver, by: str, value: str) -> WebElement:
        try:
            print(f"[DEBUG] 要素取得開始\nBy={by}\nValue={value}")
            elem = chrome.find_element(by, value)
            print(f"[DEBUG] 要素取得完了\nBy={by}\nValue={value}")
            return elem
        
        except  NoSuchElementException as e:
            print(f"[ERROR] 要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
            raise 
        
        except Exception as e:
            print(f"[ERROR] 想定外、要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
            raise 
        
    def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.ID, value)
            return elem

    def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.NAME, value)
            return elem

    def get_by_css(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement = self._find(chrome, By.CSS_SELECTOR, value)
            return elem

    def get_by_xpath(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.XPATH, value)
            return elem
        
    def get_by_class_name(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.CLASS_NAME, value)
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
    

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

class ActionElement:
    """（print版）"""

    def __init__(self) -> None:
        pass

    def send_keys(self, element: WebElement, text: str) -> None:
        try:
            print("入力開始")
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def click(self, element: WebElement) -> None:
        try:
            print("クリック開始")
            element.click()
            print("クリック完了")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def clear_and_send_keys(self, element: WebElement, text: str) -> None:
        try:
            print("入力クリア＆開始")
            element.clear()
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
        try:
            print("クリック開始")
            try:
                element.click()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                print("通常クリック不可 → JavaScriptクリックでフォールバック")
                chrome.execute_script("arguments[0].click();", element)
            print("クリック完了")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise
