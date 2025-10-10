# GEMINI


from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time

# ----------------------------------------------------
# 💡 変更点 1: loggerの代わりとしてprintを行うクラス (SimpleLogger)
# ----------------------------------------------------
class SimpleLogger:
    """loggerの代わりとしてprintを行うクラス"""
    def debug(self, msg):
        print(f"[DEBUG] {msg}")

    def error(self, msg):
        print(f"[ERROR] {msg}", file=sys.stderr)
# ----------------------------------------------------

class ActionElement:
    """Seleniumの要素操作専用クラス (init不使用版)"""

    # 💡 変更点 2: __init__ メソッドを削除
    # 初期化が不要になったため、このクラスは「単なる機能のまとまり」として使われる
    pass 
    
# --- メソッド（必ずこの順序で定義）---
# 💡 変更点 3: 全メソッドの引数に logger (SimpleLogger) を追加

    def send_keys(self, element: WebElement, text: str, logger: SimpleLogger) -> None:
        """指定の要素にテキストを入力する"""
        try:
            logger.debug("入力開始")
            element.send_keys(text)
            logger.debug(f"入力完了: {text}")
        except Exception as e:
            logger.error(f"操作失敗: {e}")
            raise

    def click(self, element: WebElement, logger: SimpleLogger) -> None:
        """指定の要素をクリックする"""
        try:
            logger.debug("クリック開始")
            element.click()
            logger.debug("クリック完了")
        except Exception as e:
            logger.error(f"操作失敗: {e}")
            raise

    def clear_and_send_keys(self, element: WebElement, text: str, logger: SimpleLogger) -> None:
        """要素をクリアしてからテキストを入力する"""
        try:
            logger.debug("入力クリア＆開始")
            element.clear()
            element.send_keys(text)
            logger.debug(f"入力完了: {text}")
        except Exception as e:
            logger.error(f"操作失敗: {e}")
            raise

    def safe_click(self, element: WebElement, chrome: WebDriver, logger: SimpleLogger) -> None:
        """
        通常クリックを試行し、失敗した場合にJavaScriptでクリックする
        :param element: 対象のWebElement
        :param chrome: WebDriverインスタンス（JavaScript実行用）
        :param logger: SimpleLoggerインスタンス
        """
        logger.debug("クリック開始")
        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            # クリックが邪魔された場合や操作不能な場合、JavaScriptでフォールバック
            logger.debug(f"クリック失敗（エラー: {type(e).__name__}）。JavaScriptで再試行。")
            try:
                # JavaScriptでクリックする
                chrome.execute_script("arguments[0].click();", element)
            except Exception as js_e:
                logger.error(f"JavaScriptクリック失敗: {js_e}")
                raise
        except Exception as e:
            # その他の予期せぬエラー
            logger.error(f"操作失敗: {e}")
            raise
        
        logger.debug("クリック完了")


# ----------------------------------------------------
# テスト実施要件（if __name__ == "__main__": ブロック）
# ----------------------------------------------------
if __name__ == "__main__":
    
    options = Options()
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"WebDriverの起動に失敗しました。Chromeドライバーのパスやバージョンを確認してください: {e}", file=sys.stderr)
        sys.exit(1)

    # 簡易ロガー（print代用）をインスタンス化
    my_logger = SimpleLogger() 
    
    # 💡 変更点 4: ActionElementのインスタンス化
    # __init__がないため、引数は不要。ただし、クラスの実体（インスタンス）は作る必要がある。
    action_element = ActionElement()
    
    target_url = "https://libecity.com/signin"
    driver.get(target_url)
    time.sleep(2)

    try:
        id_input_locator = "id_username" # ID入力欄のロケーター
        username_element = driver.find_element("id", id_input_locator)
        
        login_button_locator = "js-signin-button" # ログインボタンのロケーター
        login_button_element = driver.find_element("id", login_button_locator)
        
        test_text = "test_user_001"
        
        my_logger.debug("--- send_keysのテスト開始 ---")
        # 💡 変更点 5: メソッド呼び出し時に my_logger を引数として渡す
        action_element.send_keys(element=username_element, text=test_text, logger=my_logger)
        my_logger.debug("--- send_keysのテスト完了 ---")
        
        time.sleep(1)
        
        my_logger.debug("--- clear_and_send_keysのテスト開始 ---")
        # 💡 変更点 5: メソッド呼び出し時に my_logger を引数として渡す
        action_element.clear_and_send_keys(element=username_element, text="retest_002", logger=my_logger)
        my_logger.debug("--- clear_and_send_keysのテスト完了 ---")

        time.sleep(1)
        
        my_logger.debug("--- clickのテスト開始 ---")
        # 💡 変更点 5: メソッド呼び出し時に my_logger を引数として渡す
        action_element.click(element=login_button_element, logger=my_logger)
        my_logger.debug("--- clickのテスト完了 ---")
        
        # safe_clickのテストの呼び出し例（loggerとdriverも渡す）
        # action_element.safe_click(element=login_button_element, chrome=driver, logger=my_logger)


    except Exception as e:
        my_logger.error(f"テスト中にエラーが発生しました: {e}")
    finally:
        time.sleep(3)
        driver.quit()