import logging
from selenium import webdriver
from dotenv import load_dotenv
from flow import Flow

from simple_logger import SimpleLogger


class Main:
    """アプリ起動とFlow実行を管理するクラス"""

    def __init__(self, debug: bool = True):
        load_dotenv()
        self.logger = SimpleLogger(debugMode=debug).get_logger()
        # Chrome 起動
        self.chrome = webdriver.Chrome()
        self.logger.info("[Main] 初期化完了")

    def run(self) -> None:
        #　Flowの実行と終了処理をまとめる
        try:
            self.logger.info("[Main] Flowを開始します")
            Flow(self.chrome, self.logger).flow()
        except Exception:
            # 例外をスタックトレース付きで出力（ファイルにも保存される）
            self.logger.exception("[Main] Flow実行中に未処理例外")
        finally:
            try:
                self.chrome.quit()
                self.logger.info("[Main] Chromeを終了しました")
            except Exception:
                self.logger.exception("[Main] Chrome終了処理で例外")


if __name__ == "__main__":
    app = Main(debug=True)  # 本番運用では False 推奨（INFO以上のみ）
    app.run()