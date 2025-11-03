from selenium import webdriver
from flow import Flow
from dotenv import load_dotenv
import logging

class Main:
    """アプリ起動とFlow実行を管理するクラス"""

    def __init__(self):
        load_dotenv()                          
        self.logger = logging.getLogger("app") # ロガー（今回は未使用）
        self.chrome = webdriver.Chrome()       
        print("[Main] 初期化完了")

    def run(self):
        """Flowの実行と終了処理をまとめる"""
        try:
            Flow(self.chrome, self.logger).flow()
        finally:
            self.chrome.quit()
            print("[Main] Chromeを終了しました")

def main():
    """エントリーポイント"""
    app = Main()
    app.run()

if __name__ == "__main__":
    main()