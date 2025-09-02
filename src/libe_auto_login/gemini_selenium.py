import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ロガーの設定
# プログラムのどこで何が起きているかを記録するためのもの
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChromeDriverManager:
    """
    WebDriverの生成と管理を行うクラス
    """
    def __init__(self):
        # コンストラクタでchrome_option()を呼び出し、オプションをインスタンス変数に格納
        self.options = self.chrome_option()

    def chrome_option(self):
        """
        Chromeの起動オプションを設定
        """
        options = Options()
        # ウィンドウサイズを設定
        options.add_argument("--window-size=1280,720")
        return options

    def chrome_process(self):
        """
        webdriver.Chrome()を使い、driverを生成
        """
        try:
            # Selenium Managerが自動でドライバをセットアップ
            # コンストラクタで準備したself.optionsを引数として渡す
            driver = webdriver.Chrome(options=self.options)
            logger.info("Chromeブラウザを起動しました。")
            return driver
        except Exception as e:
            # 起動に失敗したらエラーログを記録し、処理を停止
            logger.error(f"Chromeブラウザの起動に失敗しました: {e}")
            raise

class GetElement:
    """
    WebDriverオブジェクトから要素を取得するクラス
    """
    def __init__(self, driver):
        self.driver = driver

    def get_id_element(self, element_id):
        return self.driver.find_element(By.ID, element_id)

    def get_pass_element(self, element_name):
        return self.driver.find_element(By.NAME, element_name)

    def get_check_box_element(self, element_xpath):
        return self.driver.find_element(By.XPATH, element_xpath)

    def get_login_btn_element(self, element_css):
        return self.driver.find_element(By.CSS_SELECTOR, element_css)


class ActionElement:
    """
    取得した要素に対して操作を行うクラス
    """
    def __init__(self, driver):
        self.driver = driver

    def input_element(self, element, text):
        try:
            element.send_keys(text)
            logger.info(f"要素にテキスト '{text}' を入力しました。")
        except Exception as e:
            logger.error(f"要素への入力に失敗しました: {e}")
            raise

    def click_element(self, element):
        try:
            element.click()
            logger.info("要素をクリックしました。")
        except Exception as e:
            logger.error(f"要素のクリックに失敗しました: {e}")
            raise