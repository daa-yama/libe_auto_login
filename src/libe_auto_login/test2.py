# 更新テスト

# un_selenium_demo.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def build_chrome():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    options.page_load_strategy = "eager"
    chrome = webdriver.Chrome(options=options)
    return chrome

def open_url(chrome, url, timeout=10):
    chrome.get(url)
    WebDriverWait(chrome, timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

def find_by_id(chrome, value, timeout=10):
    return WebDriverWait(chrome, timeout).until(
        EC.presence_of_element_located((By.ID, value))
    )

class GetElement:
    # __init__は使わず、呼び出し時にchromeを渡す形（関数中心の設計を崩さない）
    def by_id(self, chrome, value, timeout=10):
        return WebDriverWait(chrome, timeout).until(
            EC.presence_of_element_located((By.ID, value))
        )

if __name__ == "__main__":
    chrome = build_chrome()
    open_url(chrome, "https://www.wikipedia.org/")
    # ① 関数呼び出し → 変数に代入（推奨パターン）
    search_box = find_by_id(chrome, "searchInput")
    # ② 直書き（chrome.find_element(By.ID, value)）の動作例
    direct_box = chrome.find_element(By.ID, "searchInput")
    # 触ってみる：検索ボックスに文字を入れる（両方とも同じ要素の参照なのでどちらでも可）
    search_box.send_keys("Selenium (software)")