# main.py

from gemini_selenium import ChromeDriverManager, GetElement, ActionElement
import time
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # ChromeDriverManagerを呼び出してdriverを生成
    # ここで例外処理をしないと、driver生成失敗時にプログラムが終了してしまう
    try:
        driver_manager = ChromeDriverManager()
        driver = driver_manager.chrome_process()

        # driverを使って各クラスをインスタンス化
        get_element = GetElement(driver)
        action_element = ActionElement(driver)

        # 例としてGoogleの検索ページを開く
        driver.get("https://www.google.com")
        logger.info("Googleの検索ページを開きました。")

        # 検索ボックスの要素を取得
        # ロケータ（By.NAME）を仮に 'q' とする
        search_box = get_element.get_pass_element(element_name='q')

        # 検索ボックスにテキストを入力
        action_element.input_element(element=search_box, text="Selenium Python")

        # 検索ボックスをクリック（入力後にEnterが自動的に押される挙動を利用）
        action_element.click_element(element=search_box)

        # 動作確認のため、5秒待機
        time.sleep(5)
        
    except Exception as e:
        logger.error(f"プログラムの実行中にエラーが発生しました: {e}")
    finally:
        # 最後に必ずdriverを閉じる
        if 'driver' in locals():
            driver.quit()
            logger.info("ブラウザを閉じました。")