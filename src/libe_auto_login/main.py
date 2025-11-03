# main.py（トリガー＋最小の初期化）
from selenium import webdriver
from flow import Flow
from dotenv import load_dotenv
import logging, os

if __name__ == "__main__":
    load_dotenv()                          # (.env読み込み) ← “初期化”の範囲
    logger = logging.getLogger("app")      # （使わなくても“用意だけ”はOK）

    chrome = webdriver.Chrome()
    try:
        Flow(chrome, logger).flow()        # 業務は flow() に丸投げ
    finally:
        chrome.quit()
        
        
