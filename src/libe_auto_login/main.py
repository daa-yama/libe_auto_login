from selenium import webdriver
from my_selenium import ChromeDriverManager, GetElement, ActionElement  # selenium.py のクラスを読み込む


def main():
    # 1. Chrome を起動
    manager = ChromeDriverManager()
    driver = manager.chrome_process()

    # 2. サイトを開く（例: ログインページ）
    driver.get("https://example.com/login")
    print("[INFO] ログインページを開きました。")

    # 3. 要素取得クラスと操作クラスを準備
    getter = GetElement(driver)
    action = ActionElement(driver)

    # 4. ID / PASS / チェックボックス / ログインボタン取得
    id_box = getter.get_id_element()
    pass_box = getter.get_pass_element()
    checkbox = getter.get_check_box_element()
    login_btn = getter.get_login_btn_element()

    # 5. 値を入力＆クリック
    action.input_element(id_box, "test_user")
    action.input_element(pass_box, "password123")
    action.click_element(checkbox)
    action.click_element(login_btn)

    print("[INFO] ログインフローが完了しました。")


if __name__ == "__main__":
    main()