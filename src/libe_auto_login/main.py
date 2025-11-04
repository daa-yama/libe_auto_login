import logging

from selenium import webdriver
from dotenv import load_dotenv

from flow import Flow



class Main:
    """アプリ起動とFlow実行を管理するクラス"""

    def __init__(self):
        load_dotenv()                          # .env 読み込み
        self.logger = logging.getLogger("app") # ロガー（今回は未使用）
        self.chrome = webdriver.Chrome()       # ブラウザ起動
        print("[Main] 初期化完了")

    def run(self):
        """Flowの実行と終了処理をまとめる"""
        try:
            Flow(self.chrome, self.logger).flow()
        finally:
            self.chrome.quit()
            print("[Main] Chromeを終了しました")

if __name__ == "__main__":
    Main().run()