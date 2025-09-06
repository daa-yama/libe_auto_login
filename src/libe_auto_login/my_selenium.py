# --- 必要最小限のインポート ---
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# ========== 1) ChromeDriverManager ==========
class ChromeDriverManager:
    # ※ 型ヒントやデコレーターは使っていません
    def __init__(self, window_width=1280, window_height=800):
        self.window_width = window_width
        self.window_height = window_height

    def chrome_option(self):
        options = Options()
        # ページの読み込み完了待ちを軽めに（DOM構築で先へ進む）
        options.page_load_strategy = "eager"
        options.add_argument(f"--window-size={self.window_width},{self.window_height}")
        print(f"[INFO] Chrome のオプションを設定しました: {self.window_width}x{self.window_height}")
        return options

    def chrome_process(self):
        try:
            options = self.chrome_option()
            driver = webdriver.Chrome(options=options)  # Selenium Manager が自動解決
            # 暗黙待機は使わない（速さと安定のため）
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
    def __init__(self, driver, wait_seconds=8):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_seconds)

    def _wait_for(self, by, value, clickable=False, visible=False):
        try:
            locator = (by, value)
            if clickable:
                elem = self.wait.until(EC.element_to_be_clickable(locator))
            elif visible:
                elem = self.wait.until(EC.visibility_of_element_located(locator))
            else:
                elem = self.wait.until(EC.presence_of_element_located(locator))
            print(f"[INFO] 要素を取得しました: by={by}, value={value}")
            return elem
        except TimeoutException:
            path = "debug_not_found.png"
            try:
                self.driver.save_screenshot(path)
            except Exception:
                pass
            print(f"[ERROR] 要素が見つかりません: by={by}, value={value}")
            print(f"[DEBUG] url={self.driver.current_url}, title={self.driver.title}, screenshot={path}")
            raise

    def open_email_login_tab(self):
        # あれば一度だけ押す
        try:
            tab = self._wait_for(
                By.XPATH,
                "//*[contains(., 'メールアドレスでログイン')][self::button or self::a or self::div]",
                clickable=True,
                visible=True,
            )
            tab.click()
            print("[INFO] 『メールアドレスでログイン』タブをクリックしました。")
        except TimeoutException:
            print("[INFO] タブが見つからないのでスキップします。")

    def get_id_element(self):
        # メール欄：ORで一発
        return self._wait_for(
            By.XPATH,
            "//input[@type='email' or @name='email' "
            " or contains(@id,'mail') or contains(@name,'mail') "
            " or contains(@placeholder,'メール') or contains(@aria-label,'メール')]",
            visible=True,
        )

    def get_pass_element(self):
        # パスワード欄：ORで一発
        return self._wait_for(
            By.XPATH,
            "//input[@type='password' or @name='password' "
            " or contains(@id,'pass') or contains(@name,'pass') "
            " or contains(@placeholder,'パスワード') or contains(@aria-label,'パスワード')]",
            visible=True,
        )

    def get_check_box_element(self):
        # あれば取得。無ければ呼び出し側で例外を拾ってスキップ
        return self._wait_for(
            By.XPATH,
            "//input[@type='checkbox' or @name='remember' "
            " or //label[contains(., 'ログインしたまま')]/preceding::input[@type='checkbox'][1]]",
            clickable=True,
            visible=True,
        )

    def get_login_btn_element(self):
        # 送信ボタン：ORで一発
        return self._wait_for(
            By.XPATH,
            "//*[self::button or self::input][@type='submit' or contains(normalize-space(.),'ログイン')]",
            clickable=True,
            visible=True,
        )


# ========== 3) ActionElement ==========
class ActionElement:
    def __init__(self, driver):
        self.driver = driver

    def input_element(self, element, text, clear=True):
        try:
            if clear:
                element.clear()
            element.send_keys(text)
            print(f"[INFO] 入力しました: {text}")
        except Exception as e:
            print(f"[ERROR] 入力に失敗しました: {e}")
            raise

    def click_element(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            element.click()
            print("[INFO] 要素をクリックしました。")
        except Exception as e:
            print(f"[ERROR] クリックに失敗しました: {e}")
            raise