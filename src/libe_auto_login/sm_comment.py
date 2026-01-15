import time
# Python に最初から入っている 標準ライブラリ 時間に関する機能

import logging
#ログ出力用 

from dotenv import load_dotenv
#  load_dotenv 関数　.env ファイルを読み込んで、環境変数として使えるようにする役割。

import os
# 	OS　オペレーティングシステム（Mac）の機能を使うためのモジュール

from selenium import webdriver
# Selenium（セレニウム）は、Webブラウザの操作を自動化するためのツールセット　
# 主に、Webサイトのテスト（自動テスト）や、Web上のデータ収集（スクレイピング）で利用。
#　Selenium ライブラリから必要な機能を持ってくる。操作役

from selenium.webdriver.common.by import By
# Selenium の中の By クラスを読み込む。要素の指定方法（By~. ID, CSS, XPATH など）を一覧で持っている。
# 英語の common は共通の / よく使われる / 一般的なという意味
# Selenium ではすべてのブラウザ操作で “共通して使う機能” を集めたフォルダ（パッケージ）という意味で common という名前をつける

from selenium.webdriver.common.keys import Keys 
# キーボードの特殊キー（ENTER, TAB など）を表すクラス。element.send_keys(Keys.ENTER) のように、「Enterキーを押したことにする」ために使う

from selenium.webdriver.remote.webdriver import WebDriver
# remote の意味　リモート、遠隔　WebDriver が “別のPCやクラウドのブラウザ” でも操作できるようにする仕組み
# •	型ヒント用に WebDriver クラスを読み込んでいる。VSCode に「chrome は WebDriver 型ですよ」と教え、補完を効かせるためのもの。

from selenium.webdriver.remote.webelement import WebElement
# 型ヒント用の WebElement クラス

from selenium.webdriver.support.ui import WebDriverWait
# WebDriverWait = 要素が見つかる・クリック可能になるまで待つためのツール　Selenium の「待機」用クラス
# UI = User Interface（ユーザーインターフェース） の略。「画面操作まわりの補助」をまとめたモジュール
# サポート（support） Selenium の中でブラウザ操作を助けてくれる「便利機能」たちが入っているフォルダ

from selenium.webdriver.support import expected_conditions as EC
# Selenium の「待機専用の便利条件セット（expected_conditions）」をEC という短い名前で使えるようにする

from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
# exceptions（エクセプション）は「エラー（例外）の種類」 のこと。特定のエラーを名前で呼び出せるようにするという準備。

# ① NoSuchElementException
# →「そんな要素ありません！」エラー

# ② ElementClickInterceptedException
# →「クリックしようとしたけど、何かが邪魔して押せません！」

# ③ ElementNotInteractableException
# →「その要素、今は触れないよ！」

from simple_logger import SimpleLogger
# simple_logger.py というファイルの中にあるSimpleLogger というクラスを使えるようにする

class GetElement:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        # # 外から渡された logger を、このクラス内で使えるように保存している。logging.Logger←型ヒント
# これで self.logger.info(...) などのログ出力が使えるようになる。
# クラスに「ログ機能を持たせるための初期設定」。

    def _find(self, chrome: WebDriver, by: str, value: str) -> WebElement:
# この _find は、Chrome（WebDriver）を使って、指定された検索方法（by）と検索値（value）
# で Web 要素を探し、見つかった WebElement を返す関数
        try:
            self.logger.debug(f"[DEBUG] 要素取得開始\nBy={by}\nValue={value}")
            elem = chrome.find_element(by, value)
            self.logger.debug(f"[DEBUG] 要素取得完了\nBy={by}\nValue={value}")
            return elem

        except NoSuchElementException as e:
# 「指定した要素が画面に存在しない」ときに出るエラーがNoSuchElementException
            self.logger.error(
                f"[ERROR] 要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}"
            )
# ✔ e.__class__.__name__→ 起きたエラーの種類だけを文字で取り出す
# ✔ {e}→ エラーが持つ詳細メッセージ全文
            raise
# エラー発生の場合ここで処理を止めて呼び出し元へ戻す

        except Exception as e:
# 	•	Exception は「すべての一般的な例外の親クラス」　「NoSuchElementException 以外の、予想していないエラー」 がここに来る
            self.logger.error(
                f"[ERROR] 想定外、要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}"
            )
            raise

    def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.ID, value)
        return elem
# 	•	ID という方法で、この値の要素を探してきて！ と _find() に指示している。
# •	_find() が実際にブラウザ操作して、Web 要素（WebElement）を見つけてくる。
# •	見つかった要素を そのまま呼び出し元へ返すだけの便利ショートカット関数。

# 🎸スタッフさん、ギターケース探してきて！
# 探し方は “ケースのID番号” で！
# ID番号は「case-123」だよ！

    def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.NAME, value)
        return elem
# 	•	name 属性でこの値の要素を探して！ と _find() に指示するショートカット関数。

# 🎸“スタッフさん！
# 名前（nameタグ）で『pick-main』って書いてあるピック探してきて！”

    def get_by_css(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.CSS_SELECTOR, value)
        return elem
# CSS=HTML の中にあるタグ（input や button）を、class や id、属性などの“特徴”を使って
# ピンポイントで探し当てるための指定方法（住所のようなもの）

# 🎸スタッフさん！
# “赤いギターで、ストラトタイプで、ピックアップ3つのやつ”探してきて！

    def get_by_xpath(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.XPATH, value)
        return elem
# XPath は HTML の中の要素の位置を“パス（道順）”で指定して探す方法
# 🎸スタッフさん！“楽屋の一番奥の棚の、左から3番目のケースの中にあるギター取ってきて！”
#  これ＝ XPath での 「棚 → 段 → 位置」 を辿る指定と同じ。

    def get_by_class_name(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.CLASS_NAME, value)
        return elem
# class 属性（class=“〇〇”）で要素を探すためのショートカット関数。
# 🎸 ギターで例えると… HTML の class は「ギターのジャンルタグ」だと思えばOK。
# 例：
# 	•	class=“strat”
# 	•	class=“lespaul”
# 	•	class=“hollow”
# など。
# ⸻
# get_by_class_name の動きはこう👇
# あなた（ギタリスト）がスタッフにこう言う：
# 「ストラトタイプ（class=strat）のギターを1本持ってきて！」
# これが By.CLASS_NAME。

    def get_by_tag_name(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.TAG_NAME, value)
        return elem
# 	•	指定したタグ名（button/input など）で HTML 要素を探すショートカット関数。# 🎸 ギターに例えるなら…
# 	•	value = “strat” みたいなイメージ
# 	•	自分：「ストラトを探してきて」
# 	•	店員（_find）：店の中を探す
# 	•	自分：「ありがとう、受け取るわ」＝ return elem

    def get_by_link_text(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.LINK_TEXT, value)
        return elem
# 	•	画面に表示されているリンクの文字（例：ログイン、ホーム）で <a> 要素を探す関数。
# ページ内にこんな HTML があるとします：　
# <a href="/home">マイページ</a>　ここで "マイページ" を指定すると、そのリンク <a> 要素を取ってこれます。
#
# 🎸 ギターで例えるなら？
# リンク文字＝“ギターのモデル名ラベル”
# （タグに貼られた文字）
# 店員さん（_find）に：
# 「‘Les Paul’ って書いてあるギターを取ってきて」
# と頼むイメージ。
# → その“ラベルどおりのギター”が返ってくる。


    def get_by_partial_link_text(self, chrome: WebDriver, value: str) -> WebElement:
        elem: WebElement = self._find(chrome, By.PARTIAL_LINK_TEXT, value)
        return elem
# 	•	リンク文字の“一部だけ”を元に <a> 要素を探すための関数。
# 	•	内部では _find() に「部分一致で探して」と依頼し、見つかったリンク要素を返す。
# 🎸 ギターで例えると

# 店の棚にこう書かれていたとする：
# 	•	“Fender Stratocaster”
# 	•	“Gibson Les Paul Standard”
# 	•	“Yamaha Pacifica”

# ⸻

# あなたが言う：

# 「ストラトっぽいの持ってきて」

# 完全一致じゃないけど
# 「Strat」という 部分 が入ってるので見つかる。

# これが partial（部分一致）検索。


class ActionElement:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def send_keys(self, element: WebElement, text: str) -> None:
        """単純な入力用（クリアしない）"""
        try:
            self.logger.info("入力開始")
            element.send_keys(text)
            self.logger.info(f"入力完了: {text}")

        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise
# 	•	element に text をそのまま入力するメソッド（clearしない）。
# •	入力開始 → 実行 → 完了ログ → 失敗時はエラーを上に投げる構成。

# 🎸 ギターの例えで説明すると
# 	•	element → ギター本体
# 	•	text → 弾きたいフレーズ
# 	•	send_keys → フレーズを弾く行為
# 	•	logger → 音を録音するレコーダー

# 流れとしてはこんな感じ：
# 	1.	「今から弾きます！（logger）」
# 	2.	ギターを弾く（send_keys）
# 	3.	「今のフレーズ弾き終わりました！（logger）」
# 	4.	失敗したらエラーで知らせる（raise）


    def click(self, element: WebElement) -> None:
        try:
            self.logger.info("クリック開始")
            element.click()
            self.logger.info("クリック完了")
        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise
# 	•	クリックしたい要素を実際にクリックし、その前後にログを残すメソッド。
# 	•	失敗したらエラーをログに記録し、上にエラーを投げて処理を止める。
#  🎸 ギターで例えると…
# 	•	element → 押したいペダル
# 	•	element.click() → ペダルを踏む行為

# click() の流れはこう：
# 	1.	「ペダル踏みます！」（ログ）
# 	2.	実際にペダルを踏む
# 	3.	「踏みました！」（ログ）
# 	4.	ペダルが壊れていたら「踏めません！」と報告（except + raise）


    def clear_and_send_keys(self, element: WebElement, text: str) -> None:
        """一度クリアしてから入力する"""
        try:
            self.logger.info("入力クリア＆開始")
            element.clear()
            element.send_keys(text)
            self.logger.info(f"入力完了: {text}")

        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise
# 	入力欄をクリア → 新しい文字を入力、という“完全上書き入力”のメソッド。
# 	•	開始・完了・失敗をログに記録し、エラーがあれば上に伝える仕組み。

#  🎸 ギターの例えで説明すると…
# 	•	element.clear()
# 　→ エフェクターの設定ノブをいったん全部ゼロに戻す
# 	•	element.send_keys(text)
# 　→ 新しい音作り（設定）を入れる

# 流れとしては：
# 	1.	「設定リセットします！」（ログ）
# 	2.	ノブを全部回してゼロにする（clear）
# 	3.	新しい設定を入れる（send_keys）
# 	4.	「設定終わりました！」（ログ）
# 	5.	壊れてたら「設定できません！」と知らせる（except）

    def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
        """通常クリックがダメなときに JS クリックにフォールバック"""
        self.logger.info("クリック開始")
        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            self.logger.error(
                f"通常クリック不可（エラー種別: {type(e).__name__}）→ JavaScriptクリックでフォールバック"
            )
            try:
                chrome.execute_script("arguments[0].click();", element)
            except Exception as js_e:
                self.logger.error(f"JavaScriptクリックも失敗: {js_e}")
                raise
        except Exception as e:
            self.logger.error(f"操作失敗: {e}")
            raise
        self.logger.info("クリック完了")
        
# 	•	まず普通にクリックし、
# 	•	よくある失敗なら JavaScriptクリックに切り替え、
# 	•	それでもダメならログを残して処理を止める安全設計。
# 	•	element.click()
# → 普通にピックで弦を弾く
# 	•	ElementClickInterceptedException
# → 弦の上に手が当たって弾けない
# 	•	ElementNotInteractableException
# → 弦がミュートされてて音が出ない
# 	•	execute_script(...click...)
# → アンプのスイッチで直接音を鳴らす裏技
# 	•	それでもダメ
# → 機材トラブルなので演奏中断（raise）        


if __name__ == "__main__":
    load_dotenv()
    email = os.getenv("LOGIN_EMAIL")
    password = os.getenv("LOGIN_PASSWORD")

# 	•	if __name__ == "__main__":
# → 本番ステージのときだけ演奏するスイッチ
# 	•	.env
# → 楽屋に置いてあるセットリスト（非公開）
# 	•	os.getenv()
# → 楽屋からセットリストを取り出す    
# 	•	if __name__ == "__main__" は 直接実行時だけ動かすための条件
# 	•	load_dotenv() は .env の中身を使えるようにする
# 	•	os.getenv() は 環境変数から安全に値を取得する

    test_logger = SimpleLogger(debugMode=True).get_logger()
    
#     「デバッグ用にログ設定された logger を1つ作って、それを test_logger として使えるようにする」

# 	SimpleLogger(...)
# → アンプやエフェクターを全部セッティングする
# 	•	.get_logger()
# → 音が出る状態のギターを手に取る
# 	•	test_logger
# → 今日使うメインギター

    chrome: WebDriver = webdriver.Chrome()
    try:
        chrome.get("https://libecity.com/signin")

        ge = GetElement(test_logger)
        action = ActionElement(test_logger)

        id_input = ge.get_by_css(chrome, "input[type='text']")
        action.clear_and_send_keys(id_input, email)

        password_input = ge.get_by_css(chrome, "input[type='password']")
        action.clear_and_send_keys(password_input, password)

        login_btn = ge.get_by_xpath(
            chrome, "//button[contains(normalize-space(.), 'ログイン')]"
        )
        action.click(login_btn)

        time.sleep(3)
        test_logger.info(f"[TEST] current_url={chrome.current_url}")
    finally:
        chrome.quit()
        
# 	•	前半：ブラウザ起動 → ID / パスワード入力
# 	•	後半：ログインボタン取得 → クリック → 成功確認
# 	•	finally：成功・失敗に関係なく Chrome を閉じる安全設計

#  	•	get_by_xpath(...)
# → 「ログイン」って書いてあるペダルを探す
# 	•	action.click(login_btn)
# → そのペダルを踏む
# 	•	sleep(3)
# → 音が立ち上がるのを待つ
# 	•	current_url ログ
# → 音がちゃんと切り替わったか確認
# 	•	chrome.quit()
# → 演奏後にアンプと電源をちゃんと切る