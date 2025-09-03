# selenium.py
from __future__ import annotations

import logging
import time
from typing import Any, Callable, Tuple
from functools import wraps

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ==== logger（なければ簡易設定）====
logger = logging.getLogger("app")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(_h)
logger.setLevel(logging.DEBUG)

# ==== デバッグ用ユーティリティ ====
def _mask(text: str, keep: int = 2) -> str:
    """パスワード等の秘匿。先頭keep文字だけ残して後ろは*にする"""
    if text is None:
        return ""
    if len(text) <= keep:
        return "*" * len(text)
    return text[:keep] + "*" * (len(text) - keep)

def _elm_hint(elm: WebElement) -> str:
    """要素のログ表示用ヒント（tag, id/name, type, text一部）"""
    try:
        tag = getattr(elm, "tag_name", "?")
        _id = elm.get_attribute("id")
        _name = elm.get_attribute("name")
        _type = elm.get_attribute("type")
        _text = elm.text.strip() if hasattr(elm, "text") else ""
        if len(_text) > 20:
            _text = _text[:20] + "…"
        return f"<{tag} id={_id!r} name={_name!r} type={_type!r} text={_text!r}>"
    except Exception:
        return "<element?>"

def trace(fn: Callable[..., Any]) -> Callable[..., Any]:
    """関数の出入り・実行時間・例外を標準化して記録するデコレータ"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        # 引数のうち、文字列は長さだけ・password等はマスク
        def _fmt(v: Any) -> str:
            try:
                if isinstance(v, str):
                    key_like = any(k in fn.__name__.lower() for k in ["pass", "pwd"])
                    return f"'{_mask(v)}'" if key_like else (f"len={len(v)}" if len(v) > 50 else f"'{v}'")
                if isinstance(v, WebElement):
                    return _elm_hint(v)
                if isinstance(v, (int, float, bool, type(None))):
                    return repr(v)
                return v.__class__.__name__
            except Exception:
                return "<arg>"
        args_preview = ", ".join(_fmt(a) for a in args[1:])  # selfは除外
        kwargs_preview = ", ".join(f"{k}={_fmt(v)}" for k, v in kwargs.items())
        joined = ", ".join(x for x in [args_preview, kwargs_preview] if x)

        logger.debug(f"▶ {fn.__qualname__}({joined})")
        try:
            result = fn(*args, **kwargs)
            dt = (time.perf_counter() - t0) * 1000
            logger.debug(f"✔ {fn.__qualname__} ok ({dt:.1f} ms)")
            return result
        except Exception as e:
            dt = (time.perf_counter() - t0) * 1000
            logger.exception(f"✖ {fn.__qualname__} failed after {dt:.1f} ms: {e}")
            raise
    return wrapper


# ========== 1) ChromeDriverManager ==========
class ChromeDriverManager:
    """Selenium Manager を使って Chrome を起動して driver を返す係"""

    def __init__(self, *, window_width: int = 1280, window_height: int = 800, implicit_wait: int = 5):
        self.window_width = window_width
        self.window_height = window_height
        self.implicit_wait = implicit_wait

    @trace
    def chrome_option(self) -> Options:
        """今回はウィンドウサイズだけ設定"""
        options = Options()
        options.add_argument(f"--window-size={self.window_width},{self.window_height}")
        # ここで他のオプションも明示するとデバッグが楽（例：ヘッドレス）
        # options.add_argument("--headless=new")
        return options

    @trace
    def chrome_process(self) -> WebDriver:
        """webdriver.Chrome()（Selenium Manager）で driver を生成して返す"""
        options = self.chrome_option()
        driver = webdriver.Chrome(options=options)  # ← ドライバパス指定は不要
        if self.implicit_wait > 0:
            driver.implicitly_wait(self.implicit_wait)
        logger.debug(
            "Chrome started (implicit_wait=%ss, size=%sx%s)",
            self.implicit_wait, self.window_width, self.window_height
        )
        return driver


# ========== 2) GetElement ==========
class GetElement:
    """driver から各要素を取得して返す係（ロケータは仮実装）"""

    def __init__(self, driver: WebDriver, wait_seconds: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_seconds)
        logger.debug("GetElement initialized (wait=%ss, url=%s)", wait_seconds, driver.current_url)

    @trace
    def _wait_for(self, by: By, value: str, *, clickable: bool = False) -> WebElement:
        mode = "clickable" if clickable else "presence"
        logger.debug("Waiting for element (%s): by=%s, value=%s", mode, by, value)
        elm = self.wait.until(
            EC.element_to_be_clickable((by, value)) if clickable
            else EC.presence_of_element_located((by, value))
        )
        logger.debug("Found element: %s", _elm_hint(elm))
        return elm

    # --- 要件の4メソッド（ロケータは例：実サイトに合わせて差し替え）---
    @trace
    def get_id_element(self) -> WebElement:
        # 例: <input id="user_id">
        return self._wait_for(By.ID, "user_id")

    @trace
    def get_pass_element(self) -> WebElement:
        # 例: <input id="password" type="password">
        return self._wait_for(By.ID, "password")

    @trace
    def get_check_box_element(self) -> WebElement:
        # 例: <input name="remember_me" type="checkbox">
        return self._wait_for(By.NAME, "remember_me", clickable=True)

    @trace
    def get_login_btn_element(self) -> WebElement:
        # 例: <button type="submit">ログイン</button>
        try:
            return self._wait_for(By.CSS_SELECTOR, "button[type='submit']", clickable=True)
        except TimeoutException:
            logger.debug("Primary login button not found; fallback to input[type=submit]")
            return self._wait_for(By.CSS_SELECTOR, "input[type='submit']", clickable=True)


# ========== 3) ActionElement ==========
class ActionElement:
    """取得した要素に対して入力・クリック等を行う係"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.debug("ActionElement initialized (url=%s)", driver.current_url)

    @trace
    def input_element(self, element: WebElement, text: str, *, clear: bool = True, secret: bool = False) -> None:
        # textのログは秘匿可能
        shown = _mask(text) if secret else (f"{len(text)} chars" if len(text) > 30 else repr(text))
        logger.debug("Input target: %s | text=%s | clear=%s", _elm_hint(element), shown, clear)
        if clear:
            element.clear()
        element.send_keys(text)
        logger.debug("Input done on: %s", _elm_hint(element))

    @trace
    def click_element(self, element: WebElement) -> None:
        logger.debug("Click target: %s", _elm_hint(element))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.click()
        logger.debug("Clicked: %s", _elm_hint(element))