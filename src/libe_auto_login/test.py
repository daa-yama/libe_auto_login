# main_test.py （例）
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium_manager import GetElement   # あなたのファイル名に合わせて

def run():
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.google.com/")
        getter = GetElement()

        # 1) 正常系
        print("=== 正常系: name='q' ===")
        elem = getter.get_by_name(driver, "q")  # driver, "q"
        print("tag_name:", elem.tag_name)                 # elem.tag_name
        print("name attr:", elem.get_attribute("name"))                # elem.get_attribute("name")
        # 文字入力して見た目で確認
        elem.send_keys("Selenium Python")        # elem

        # 2) 失敗系
        print("=== 失敗系: name='q_not_found' ===")
        try:
            getter.get_by_name(driver, "q_not_found")     # driver, "q_not_found"
        except NoSuchElementException:
            print("OK: 期待通りに例外が伝播した")
        else:
            print("NG: 例外が出ずに通ってしまった")

    finally:
        driver.quit()

if __name__ == "__main__":
    run()