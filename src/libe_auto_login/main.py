from selenium.common.exceptions import TimeoutException
#ページの要素が見つからず、待つ時間が終わってしまったという、特定のエラーが起きたときに、それに対応するための道具

from my_selenium import ChromeDriverManager, GetElement, ActionElement
# 自作モジュール my_selenium から、
# ChromeDriverManager（ブラウザ）, GetElement（要素）, ActionElement（入力） という3つのクラスをインポート


def main():
    # プログラムの入口となる関数 main を定義
    
    manager = ChromeDriverManager()
    # ChromeDriverManager のインスタンスを作成。manager という変数に保存
    
    driver = manager.chrome_process()
    # ChromeDriver を起動して、driver という変数に保存　
    # driver はブラウザのリモコン。get(), quit() などの操作が可能

    try:
        # この後の処理でエラーが出ても、最後に後片付け（finally）を必ず実行するための枠。
        # try/except/finally：問題が出るかもしれない場所を保護する構文
        
        driver.get("https://libecity.com/signin")
        # ChromeDriver で指定した URL を開く
        
        print("[INFO] ログインページを開きました。")
        # ログインページを開いたことを知らせるメッセージを表示

        getter = GetElement(driver, wait_seconds=8)
        # 要素を探す係。ページ内の入力欄やボタンを待ちながら取得。
        # GetElement のインスタンスを作成。driver と 待ち時間 8秒 を渡す
        
        action = ActionElement(driver)
        # 操作担当（文字入力・クリック）を作成。•取得（GetElement）と操作（ActionElement）を役割分担。
        # ActionElement のインスタンスを作成。driver を渡す

        # タブは一度だけ
        getter.open_email_login_tab()
        # メールアドレスでログインするタブを開く（初期状態で開いていない場合があるため）

        # 入力欄の取得
        id_box = getter.get_id_element()
        # ユーザーID入力欄の要素を探して取得    
        
        pass_box = getter.get_pass_element()
        # パスワード入力欄の要素を探して取得

        # 任意：チェックボックスは無ければスキップ
        try:
            checkbox = getter.get_check_box_element()
            #  チェックボックスの要素を探して取得
        
            action.click_element(checkbox)
            #  見つけたチェックボックスをクリック
        
        except TimeoutException:
            # 要素が見つからず、待つ時間が終わってしまった場合のエラーをキャッチ
        
            print("[INFO] チェックボックスなし。スキップ。")
            # チェックボックスが無かったことを知らせるメッセージを表示

        # ボタン取得
        login_btn = getter.get_login_btn_element()
        # ログインボタンの要素を探して取得

        # 入力 → 送信
        action.input_element(id_box, "example_user")
        #   ユーザーID入力欄に "example_user" を入力
        
        action.input_element(pass_box, "secret_password")
        #   パスワード入力欄に "secret_password" を入力
        
        action.click_element(login_btn)
        #   ログインボタンをクリック

        print("[INFO] ログインフローが完了しました。")
        # ログインフローが完了したことを知らせるメッセージを表示
        
        input("画面を確認したら Enter ▶ ")
        # 画面を確認するために一時停止。Enter キーが押されるまで待つ

    finally:
        # エラーの有無にかかわらず、最後に必ず実行される後片付け
        
        driver.quit()
        # ChromeDriver を終了して、ブラウザを閉じる　
        # close との違い：close はタブを閉じる、quit はプロセスごと終了。終了漏れはPCを重くする原因に


if __name__ == "__main__":
    main()
    # このファイルが直接実行された場合に main() を呼び出す          
    
    
    
    
    
    
    
    
    
    # 用語のやさしいミニ辞書
	# •	モジュール：Python ファイル。機能をまとめた部品箱。
	# •	クラス / インスタンス：設計図がクラス、そこから作った実体がインスタンス。
	# •	メソッド：インスタンスに紐づいた関数。driver.get() など。
	# •	例外（Exception）：おかしな事態が起きた合図。try/except で分岐処理ができる。
	# •	TimeoutException：待ち時間切れの例外。要素が出てこない時に発生。
	# •	セレクタ（CSS/XPath）：ページ内で要素を指定するための文字列。
	# •	WebDriver：ブラウザを遠隔操作するためのリモコン的オブジェクト。
 
#  仕上げのチェックリスト
# 	•	my_selenium.py が正しい場所にあり、クラス名が一致している
# 	•	Chrome/Driver のバージョン整合が取れている（ChromeDriverManager 側で対応）
# 	•	ログイン要素のセレクタが現行ページに合っている（UI 変更時は GetElement を修正）
# 	•	資格情報は直書きしない（環境変数や設定ファイルへ）
# 	•	失敗時でも driver.quit() が必ず呼ばれる（try/finally で担保）