# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# import
import logging
from datetime import datetime


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class LoggerBasicColor(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[90m",  # グレー
        "INFO": "\033[94m",  # 青色
        "WARNING": "\033[93m",  # 黄色
        "ERROR": "\033[91m",  # 赤色
        "CRITICAL": "\033[95m",  # マゼンダ
    }
    # 基本の色
    RESET = "\033[0m"

    # ----------------------------------------------------------------------------------
    # loggingのformatをカスタムしてログレベルに応じた色付けを行う

    def format(self, record):
        message = super().format(record)  # 親クラス logging.Formatter の format を呼び出す
        color = self.COLORS.get(record.levelname, "")  # 色を取得
        return f"{color}{message}{self.RESET}"


# ----------------------------------------------------------------------------------
# **********************************************************************************



class SimpleLogger:
    def __init__(self, debugMode: bool=True):
        self.logger = logging.getLogger(__name__)

        self.loggingLevel = logging.DEBUG if debugMode else logging.INFO
        self.logger.setLevel(self.loggingLevel)

        # インスタンス
        self.currentDate = datetime.now().strftime('%y%m%d')
        self.setUpToLogger()  # addHandlerにて追加したものを反映


    # ----------------------------------------------------------------------------------
    # カスタムされたloggerをセットする

    def setUpToLogger(self):
        if not self.logger.handlers:
            # ログをコンソール（ターミナル）に表示させる設定
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(self.loggingLevel)

            # ログメッセージの基本フォーマット→時間→ログレベル→エラーメッセージ
            consoleHandler.setFormatter(LoggerBasicColor("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(consoleHandler)

            # ログFileを出力を定義
            # 拡張する際にはここのPathを変更する
            log_file_path = f"{self.currentDate}Debug.log"

            # ログをファイルに出力させる設定
            fileHandler = logging.FileHandler(log_file_path, encoding="utf-8")
            fileHandler.setLevel(logging.DEBUG)
            fileHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(fileHandler)

            # ログの出力を重複させない設定
            self.logger.propagate = False

    # ----------------------------------------------------------------------------------
    # カスタムされたLoggerを取得する

    def get_logger(self):
        return self.logger

    # ----------------------------------------------------------------------------------

    # 呼び出す際
    # from method.base.utils.logger import SimpleLogger
    # でimportして

    # 対象のクラスのinit内で
    # self.logger_setup = SimpleLogger()
    # self.logger = self.logger_setup.get_logger()
    # を定義

    # 実際のコードでは
    # self.logger.info("ログメッセージ")
    # self.logger.debug("デバッグメッセージ")
    # self.logger.warning("警告メッセージ")
    # self.logger.error("エラーメッセージ")
    # self.logger.critical("重大なエラーメッセージ")


# **********************************************************************************

if __name__ == "__main__":
    # テストコード
    test_logger = SimpleLogger(debugMode=True)
    logger = test_logger.get_logger()

    logger.debug("これはデバッグメッセージです")
    logger.info("これは情報メッセージです")
    logger.warning("これは警告メッセージです")
    logger.error("これはエラーメッセージです")
    logger.critical("これは重大なエラーメッセージです")
