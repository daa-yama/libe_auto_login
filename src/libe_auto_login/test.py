# ChatGPT


from __future__ import annotations

import time
from typing import Iterable, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)


class ActionElement:
    """要素に対する操作だけを担当するクラス（printでログ出力する簡易版）。"""

    def __init__(self) -> None:
        """この学習版では logger を使わないので、特に保持する状態はありません。"""
        pass

    def send_keys(self, element: WebElement, text: str) -> None:
        """指定要素に文字列を入力する。操作前後でログを出す。"""
        try:
            print("入力開始")
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:  # 予期しない例外も含めて必ず伝播
            print(f"操作失敗: {e}")
            raise

    def click(self, element: WebElement) -> None:
        """指定要素をクリックする。操作前後でログを出す。"""
        try:
            print("クリック開始")
            element.click()
            print("クリック完了")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def clear_and_send_keys(self, element: WebElement, text: str) -> None:
        """一度クリアしてから入力する。操作前後でログを出す。"""
        try:
            print("入力クリア＆開始")
            element.clear()
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
        """通常クリックが妨げられたら JS クリックでフォールバックする安全版。"""
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


# --- 補助関数（学習用）: 候補ロケータを順に試して最初に見つかった要素を返す ---

def find_first(chrome: WebDriver, candidates: Iterable[Tuple[str, str]], timeout: int = 10) -> WebElement:
    last_error: Exception | None = None
    for by, value in candidates:
        try:
            return WebDriverWait(chrome, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as e:
            last_error = e
    # どれも見つからなかった場合は最後のエラーを再送出
    if last_error:
        raise last_error
    raise TimeoutException("No candidates matched.")


# --- ロケータ候補（対象ページのDOM変化に多少強いように複数用意） ---

ID_INPUT_CANDIDATES = [
    (By.ID, "email"),
    (By.NAME, "email"),
    (By.CSS_SELECTOR, "input[type='email']"),
    (By.ID, "username"),
    (By.NAME, "username"),
    (By.CSS_SELECTOR, "input[autocomplete='username']"),
    (By.CSS_SELECTOR, "input[type='text']"),
]

LOGIN_BUTTON_CANDIDATES = [
    (By.CSS_SELECTOR, "button[type='submit']"),
    (By.XPATH, "//button[contains(., 'ログイン')]")
    ,
    (By.XPATH, "//button[contains(., 'Login') or contains(., 'Sign in') or contains(., 'サインイン')]")
    ,
    (By.CSS_SELECTOR, "input[type='submit']"),
]


# --- GetElement が未実装でもテストできるように学習用の簡易版を同名で用意 ---
try:
    GetElement  # 既にどこかで定義済みならそれを使う
except NameError:  # なければ簡易版を定義
    class GetElement:
        def __init__(self, chrome: WebDriver) -> None:
            self.chrome = chrome

        def first(self, candidates: Iterable[Tuple[str, str]], timeout: int = 10) -> WebElement:
            return find_first(self.chrome, candidates, timeout)


# --- 簡易テスト（課題指示どおり末尾に設置） ---
if __name__ == "__main__":
    # 1) Chrome 起動
    chrome: WebDriver = webdriver.Chrome()

    try:
        # 2) 対象ページへ
        chrome.get("https://libecity.com/signin")

        # 3) GetElement を用意
        ge = GetElement(chrome)

        # 4) ID入力欄の取得（候補を順に試す）
        id_input: WebElement = ge.first(ID_INPUT_CANDIDATES, timeout=15)

        # 5) 操作用クラスの用意（print版）
        action = ActionElement()

        # 6) クリアしてから任意の文字列を入力
        action.clear_and_send_keys(id_input, "test@example.com")

        # 7) ログインボタンを取得
        login_btn: WebElement = ge.first(LOGIN_BUTTON_CANDIDATES, timeout=15)

        # 8) 安全クリック（通常→JSフォールバック）
        action.safe_click(login_btn, chrome)

        # 9) 観察用に少し待つ（学習用途）
        time.sleep(2)

    finally:
        # 10) 終了
        chrome.quit()