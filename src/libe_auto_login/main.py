from selenium.common.exceptions import TimeoutException
from my_selenium import ChromeDriverManager, GetElement, ActionElement

def main():
    manager = ChromeDriverManager()
    driver = manager.chrome_process()
    try:
        driver.get("https://libecity.com/signin")
        print("[INFO] ログインページを開きました。")

        getter = GetElement(driver, wait_seconds=5)
        action  = ActionElement(driver)

        # 文脈の準備（タブ→必要ならiframeへ）
        getter.open_email_login_tab()  # 中で失敗しても安全

        # 入力欄取得
        id_box  = getter.get_id_element()
        pass_box= getter.get_pass_element()

        # （任意）チェックボックス
        try:
            checkbox = getter.get_check_box_element()
            action.click_element(checkbox)
        except TimeoutException:
            print("[INFO] チェックボックスなし。スキップ。")

        # 送信ボタン
        login_btn = getter.get_login_btn_element()

        # 入力→送信
        action.input_element(id_box,  "test_user@example.com")
        action.input_element(pass_box,"password123")
        action.click_element(login_btn)

        print("[INFO] ログインフローが完了しました。")
        input("画面を確認したら Enter ▶ ")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()