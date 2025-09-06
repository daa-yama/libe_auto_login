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

    def __init__(self, driver: WebDriver, wait_seconds: int = 5):  # ★ 少し長め
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_seconds)

    def _wait_for(self, by: By, value: str, *, clickable: bool = False, visible: bool = False) -> WebElement:
        try:
            locator = (by, value)
            if clickable:
                elem = self.wait.until(EC.element_to_be_clickable(locator))
            elif visible:  # ★ “見える”まで待つ（presenceだけだと表示前に取れてしまう）
                elem = self.wait.until(EC.visibility_of_element_located(locator))
            else:
                elem = self.wait.until(EC.presence_of_element_located(locator))

            print(f"[INFO] 要素を取得しました: by={by}, value={value}")
            return elem
        except TimeoutException:
            path = "debug_not_found.png"
            self.driver.save_screenshot(path)
            print(f"[ERROR] 要素が見つかりません: by={by}, value={value}")
            print(f"[DEBUG] url={self.driver.current_url}, title={self.driver.title}, screenshot={path}")
            raise

    # --- 追加: メールログインの“文脈”へ入る (タブ開く + iframeに入る) ---
    def open_email_login_tab(self) -> None:
        """『メールアドレスでログイン』タブを開く（存在すれば）"""
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

    def _switch_into_frame_that_has_email(self) -> bool:
        """★ email入力欄を含む iframe を自動検出して switch_to.frame する"""
        from selenium.webdriver.common.by import By
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        print(f"[DEBUG] iframe count: {len(frames)}")
        for i, fr in enumerate(frames):
            # 各フレームに入って探す
            self.driver.switch_to.frame(fr)
            try:
                self.wait.until(EC.presence_of_element_located((
                    By.XPATH,
                    "//input[@type='email' or contains(@name,'mail') or contains(@id,'mail') or @autocomplete='username']",
                )))
                print(f"[INFO] email欄を含む iframe を検出: index={i}")
                return True
            except TimeoutException:
                # 戻って次のiframeへ
                self.driver.switch_to.default_content()
                continue
        return False

    def _ensure_email_context(self) -> None:
        """★ タブ開く→(必要なら)該当iframeへ入る→フォームのコンテナ可視まで待つ"""
        # 1) タブ（必要なら）
        self.open_email_login_tab()

        # 2) まずは親ドキュメントで可視のコンテナを待つ（あれば）
        try:
            self._wait_for(
                By.XPATH,
                "//*[contains(., 'メール') and (self::form or self::div)][.//input]",
                visible=True
            )
        except TimeoutException:
            pass  # 無くてもOK

        # 3) 見つからなければ iframe を総当りして中に入る
        found_in_frame = self._switch_into_frame_that_has_email()
        if not found_in_frame:
            # 念のため親に戻して続行（親にあるケースもある）
            self.driver.switch_to.default_content()

    def get_id_element(self) -> WebElement:
        self.driver.switch_to.default_content()  # ★ 一旦親に戻す（多重frame回避）
        self._ensure_email_context()             # ★ 文脈準備

        # ★ フォールバックを強化（placeholder/aria-label/日本語対応）
        candidates = [
            (By.NAME, "email"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.XPATH, "//input[@autocomplete='username']"),
            (By.XPATH, "//input[contains(@id,'mail') or contains(@name,'mail')]"),
            (By.XPATH, "//input[contains(@placeholder,'メール') or contains(@aria-label,'メール')]"),
            (By.XPATH, "//label[contains(., 'メール')]/following::input[1]"),
        ]
        for by, value in candidates:
            try:
                return self._wait_for(by, value, visible=True)
            except TimeoutException:
                continue

        print("[ERROR] email入力欄が見つかりませんでした。")
        raise TimeoutException("email field not found")

    def get_pass_element(self) -> WebElement:
        # パスワードは email と同じ場所にあると想定。frameは触らずそのまま探す
        candidates = [
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.XPATH, "//input[@autocomplete='current-password' or @autocomplete='new-password']"),
            (By.XPATH, "//input[contains(@id,'pass') or contains(@name,'pass')]"),
            (By.XPATH, "//input[contains(@placeholder,'パスワード') or contains(@aria-label,'パスワード')]"),
            (By.XPATH, "//label[contains(., 'パスワード')]/following::input[1]"),
        ]
        for by, value in candidates:
            try:
                return self._wait_for(by, value, visible=True)
            except TimeoutException:
                continue

        print("[ERROR] password入力欄が見つかりませんでした。")
        raise TimeoutException("password field not found")

    def get_check_box_element(self) -> WebElement:
        candidates = [
            (By.NAME, "remember"),
            (By.CSS_SELECTOR, "input[type='checkbox']"),
            (By.XPATH, "//label[contains(., 'ログインしたまま')]/preceding::input[@type='checkbox'][1]"),
        ]
        for by, value in candidates:
            try:
                return self._wait_for(by, value, clickable=True, visible=True)
            except TimeoutException:
                continue
        print("[INFO] チェックボックスが見つからないのでスキップします。")
        raise TimeoutException("remember checkbox not found")

    def get_login_btn_element(self) -> WebElement:
        candidates = [
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//*[self::button or self::input][@type='submit' or contains(., 'ログイン')]"),
        ]
        for by, value in candidates:
            try:
                return self._wait_for(by, value, clickable=True, visible=True)
            except TimeoutException:
                continue
        print("[ERROR] ログインボタンが見つかりませんでした。")
        raise TimeoutException("login button not found")
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