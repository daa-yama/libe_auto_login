from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

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