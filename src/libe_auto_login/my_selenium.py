# selenium_utils.py などのファイル名で保存（※ "selenium.py" だと本家seleniumと衝突するので注意）

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver


# ---- logger の準備（なければ簡易的に）----
logger = logging.getLogger("app")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class ChromeDriverManager:
    """
    Chromeブラウザの起動を担当するクラス
    - Selenium Manager を利用するので driverパス指定は不要
    - 起動失敗時は logger.error で記録し raise で停止
    """

    def __init__(self, *, window_width: int = 1280, window_height: int = 800, implicit_wait: int = 5):
        self.window_width = window_width
        self.window_height = window_height
        self.implicit_wait = implicit_wait

    def chrome_option(self) -> Options:
        """Chrome起動オプションを作成（今回はウィンドウサイズのみ）"""
        try:
            options = Options()
            options.add_argument(f"--window-size={self.window_width},{self.window_height}")
            return options
        except Exception as e:
            logger.error("Failed to build Chrome options: %s", e, exc_info=True)
            raise

    def chrome_process(self) -> WebDriver:
        """driverを生成して返す"""
        try:
            options = self.chrome_option()
            driver = webdriver.Chrome(options=options)  # Selenium Manager が自動でドライバを解決
            if self.implicit_wait > 0:
                driver.implicitly_wait(self.implicit_wait)
            logger.debug("Chrome driver started successfully.")
            return driver
        except WebDriverException as e:
            logger.error("Failed to start Chrome via Selenium Manager: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error while creating Chrome driver: %s", e, exc_info=True)
            raise