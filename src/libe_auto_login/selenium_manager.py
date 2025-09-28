# ////////
dl和kjfkl邪wg；k邪h；fh
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

class GetElement:
    def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}" ) 
            elem = chrome.find_element(By.ID, "username")
            print(f"要素取得完了: \n{value}") 
            return elem
        
        except  NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e
        
        except Exception as e:
            print(f"想定外、要素取得失敗: \n{e}")
            raise e
        
    def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}" ) 
            elem = chrome.find_element(By.NAME, value)
            print(f"要素取得完了: \n{value}") 
            return elem
        
        except  NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e
        
        except Exception as e:
            print(f"想定外、要素取得失敗: \n{e}")
            raise e
        

        # def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:
    
    # def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
    
    # def get_by_css(self, chrome: WebDriver, value: str) -> WebElement:
    
    # def get_by_xpath(self, chrome: WebDriver, value: str) -> WebElement:
    
    # def get_by_class_name(self, chrome: WebDriver, value: str) -> WebElement:

    # def get_by_tag_name(self, chrome: WebDriver, value: str) -> WebElement:
        
    # def get_by_link_text(self, chrome: WebDriver, value: str) -> WebElement:

    # def get_by_partial_link_text(self, chrome: WebDriver, value: str) -> WebElement:
















































# #chatGPTが出したコード
# # selenium_manager.py
# from __future__ import annotations

# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webdriver import WebDriver
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException, WebDriverException


# class GetElement:
#     """
#     要素取得専用クラス（学習用：printで前後ログを出す版）
#     ※ 今回は logger 未使用。のちに print を logger.debug/error に置換するだけで移行できる設計。
#     """

#     def __init__(self, chrome: WebDriver, logger=None) -> None:
#         # 要件：__init__(self, chrome, logger) で受け取るが、今回は print 学習版のため logger は保持のみ
#         self.chrome: WebDriver = chrome
#         self.logger = logger

#     # --- 内部共通関数：前後ログ＋例外処理を1か所に集約 ---
#     def _find(self, by: str, value: str) -> WebElement:
#         print(f"[DEBUG] 要素取得開始:\nBy={by}\nValue={value}")
#         try:
#             element: WebElement = self.chrome.find_element(by, value)
#             print(f"[DEBUG] 要素取得完了:\nBy={by}\nValue={value}")
#             return element
#         except (NoSuchElementException, WebDriverException) as e:
#             print(f"[ERROR] 要素取得失敗(既知例外):\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
#             raise
#         except Exception as e:
#             # 予期しない例外もログして必ず上に伝える
#             print(f"[ERROR] 要素取得失敗(想定外例外):\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
#             raise

#     # 以降は要件順で個別メソッドを定義（中身は共通関数に委譲）
#     def get_by_id(self, value: str) -> WebElement:
#         return self._find(By.ID, value)

#     def get_by_name(self, value: str) -> WebElement:
#         return self._find(By.NAME, value)

#     def get_by_css(self, value: str) -> WebElement:
#         return self._find(By.CSS_SELECTOR, value)

#     def get_by_xpath(self, value: str) -> WebElement:
#         return self._find(By.XPATH, value)

#     def get_by_class_name(self, value: str) -> WebElement:
#         return self._find(By.CLASS_NAME, value)

#     def get_by_tag_name(self, value: str) -> WebElement:
#         return self._find(By.TAG_NAME, value)

#     def get_by_link_text(self, value: str) -> WebElement:
#         return self._find(By.LINK_TEXT, value)

#     def get_by_partial_link_text(self, value: str) -> WebElement:
#         return self._find(By.PARTIAL_LINK_TEXT, value)
    
    
    
    
# #Geminiが出したコード 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webdriver import WebDriver
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException

# class GetElement:
#     def __init__(self, chrome: WebDriver):
#         self.chrome = chrome

#     def get_by_id(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.ID, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_name(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.NAME, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_css(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.CSS_SELECTOR, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_xpath(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.XPATH, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_class_name(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.CLASS_NAME, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_tag_name(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.TAG_NAME, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_link_text(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.LINK_TEXT, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_partial_link_text(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.PARTIAL_LINK_TEXT, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e