from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# ========== 1) ChromeDriverManager ==========
class ChromeDriverManager:
    """Selenium Manager を使って Chrome を起動して driver を返す係（print版）"""

    def __init__(self, *, window_width: int = 1280, window_height: int = 800, implicit_wait: int = 5):
        self.window_width = window_width
        self.window_height = window_height
        self.implicit_wait = implicit_wait

    def chrome_option(self) -> Options:
        options = Options()
        options.add_argument(f"--window-size={self.window_width},{self.window_height}")
        print(f"[INFO] Chrome のオプションを設定しました: {self.window_width}x{self.window_height}")
        return options

    def chrome_process(self) -> WebDriver:
        try:
            options = self.chrome_option()
            driver = webdriver.Chrome(options=options)  # ドライバパス指定は不要
            if self.implicit_wait > 0:
                driver.implicitly_wait(self.implicit_wait)
            print("[INFO] Chrome driver が正常に起動しました。")
            return driver
        except WebDriverException as e:
            print(f"[ERROR] Chrome 起動に失敗しました: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Chrome 起動中に予期せぬエラー: {e}")
            raise


# ========== 2) GetElement ==========
class GetElement:
    """driver から各要素を取得して返す係（print版）"""

    def __init__(self, driver: WebDriver, wait_seconds: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_seconds)

    def _wait_for(self, by: By, value: str, *, clickable: bool = False) -> WebElement:
        try:
            if clickable:
                elem = self.wait.until(EC.element_to_be_clickable((by, value)))
            else:
                elem = self.wait.until(EC.presence_of_element_located((by, value)))
            print(f"[INFO] 要素を取得しました: by={by}, value={value}")
            return elem
        except TimeoutException:
            print(f"[ERROR] 要素が見つかりません: by={by}, value={value}")
            raise

    def get_id_element(self) -> WebElement:
        return self._wait_for(By.ID, "user_id")

    def get_pass_element(self) -> WebElement:
        return self._wait_for(By.ID, "password")

    def get_check_box_element(self) -> WebElement:
        return self._wait_for(By.NAME, "remember_me", clickable=True)

    def get_login_btn_element(self) -> WebElement:
        try:
            return self._wait_for(By.CSS_SELECTOR, "button[type='submit']", clickable=True)
        except TimeoutException:
            return self._wait_for(By.CSS_SELECTOR, "input[type='submit']", clickable=True)


# ========== 3) ActionElement ==========
class ActionElement:
    """取得した要素に対して入力・クリック等を行う係（print版）"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def input_element(self, element: WebElement, text: str, *, clear: bool = True) -> None:
        try:
            if clear:
                element.clear()
            element.send_keys(text)
            print(f"[INFO] 入力しました: {text}")
        except Exception as e:
            print(f"[ERROR] 入力に失敗しました: {e}")
            raise

    def click_element(self, element: WebElement) -> None:
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            element.click()
            print("[INFO] 要素をクリックしました。")
        except Exception as e:
            print(f"[ERROR] クリックに失敗しました: {e}")
            raise