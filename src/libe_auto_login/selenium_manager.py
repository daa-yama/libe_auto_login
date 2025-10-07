from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

class GetElement:
    def _find(self, chrome:WebDriver, by: str, value: str) -> WebElement:
        try:
            print(f"[DEBUG] 要素取得開始\nBy={by}\nValue={value}")
            elem = chrome.find_element(by, value)
            print(f"[DEBUG] 要素取得完了\nBy={by}\nValue={value}")
            return elem
        
        except  NoSuchElementException as e:
            print(f"[ERROR] 要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
            raise 
        
        except Exception as e:
            print(f"[ERROR] 想定外、要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
            raise 
        
    def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.ID, value)
            return elem

    def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.NAME, value)
            return elem

    def get_by_css(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement = self._find(chrome, By.CSS_SELECTOR, value)
            return elem

    def get_by_xpath(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.XPATH, value)
            return elem
        
    def get_by_class_name(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement =  self._find(chrome, By.CLASS_NAME, value)
            return elem

    def get_by_tag_name(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement = self._find(chrome, By.TAG_NAME, value)
            return elem
        
    def get_by_link_text(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement = self._find(chrome, By.LINK_TEXT, value)
            return elem

    def get_by_partial_link_text(self, chrome: WebDriver, value: str) -> WebElement:
            elem: WebElement = self._find(chrome, By.PARTIAL_LINK_TEXT, value)
            return elem
        

# from selenium.webdriver.common.by import By

# Selenium の中にある webdriver 機能のうちcommon (共通) の仕組みから
# By という　要素の検索方法を定義した設計図（クラス）を取り込んでいます
# By~（例：By.ID, By.NAME, By.CSS_SELECTOR, By.XPATH）

# from selenium.webdriver.remote.webdriver import WebDriver

# Selenium の中にある webdriver 機能のうち、remote (遠隔操作) をするための仕組みから
# WebDriver というブラウザ操作の設計図（クラス）を取り込んでいます
# remote = ネットワーク越しのブラウザ操作を可能にするモジュール(遠隔操作)
# webdriverはWebブラウザを操作するインターフェース

# from selenium.webdriver.remote.webelement import WebElement

# seleniumの中にあるwebdriver機能のうちremoteリモートで動かす仕組みから
# WebElement というブラウザ上の要素（ボタンや入力欄など）を表す設計図（クラス）で、
# find_element() の結果として実際に返ってくるオブジェクトです

# from selenium.common.exceptions import NoSuchElementException

# Selenium の中にある common (共通) の例外（エラー）の仕組みから、
# NoSuchElementException という「要素が見つからなかった」というエラーの設計図（クラス）を取り込んでいます。
# （要素が見つからないときに出るエラーをインポートしている）
# 	selenium.common.exceptions は Selenium が用意している「エラーの種類（例外クラス）」がまとめられているモジュール。
# 	その中の NoSuchElementException は「find_element で指定した要素が見つからないときに自動で投げられるエラー」。
# 	これを except NoSuchElementException: で受け止めることで、エラーになって処理が止まるのを防ぎ、ログを出したりリトライしたりできる。


# class GetElement:

#     def _find(self, chrome:WebDriver, by: str, value: str) -> WebElement:

# ＿findという探すメソッドを定義。それぞれの引数selfはクラス自身、chrome:Webdriverはブラウザを操作するオブジェクト、
# by: strで検索方法（By.IDやBy.XPATHなど）を文字列で受け取り、
# value: strで検索する実際の値（ID名やCSSセレクタなど　例: "username", "q"）を文字列で受け取る。それをWebElementに返している。
# str = stringsの略。文字列が入りますよという型ヒント。　-> 〇〇 = 〇〇を戻すという目印 


#         try:

# 要素の検索を試み、成功すれば要素を返却する
# ここから先の処理で失敗（例外）が起きるかもしれないので、「見張りモード」で実行する合図
# try: のブロック内でエラーが起きると、以降の行は実行されず、対応する except にジャンプ
# 	後続の print や return が実行されるのは成功した場合だけ


#             print(f"[DEBUG] 要素取得開始\nBy={by}\nValue={value}")

# これから探しに行く条件を記録する「開始ログ」
# \n は改行。読みやすさの為
# 将来的に 本番用にprint を logger.debug に置き換える
# デバッグ時、「何を探しに行ったのか」がわかる

#             elem = chrome.find_element(by, value)

# WebDriver（chrome）に「by という探し方で、value という具体値を探せ」と命令
# •	例：by=By.ID, value="username" なら、id="username" の要素を探します。
# •	見つかれば、右辺の結果（WebElement オブジェクト）が左の elem に代入されます。
# •	見つからないときはここで例外（NoSuchElementException など）が発生し、下の行はスキップされて except に移動します。


#             print(f"[DEBUG] 要素取得完了\nBy={by}\nValue={value}")

# 検索が成功した直後に出す「完了ログ」

#             return elem

# 見つけた WebElement を呼び出し元へ返す行
# return に到達した時点で関数は終了 その後の行は実行されない
# 
#         except  NoSuchElementException as e:

# try ブロック内で、「探している要素がWebページ上に存在しない」という特定の失敗（NoSuchElementException）が発生した場合に、
# この処理を開始。発生したエラーオブジェクトをeという変数に代入

# ・　except: tryブロックの中でエラー（例外）が起きた場合に、ここで受け止めて処理するためのキーワード　例外が起きなければこの行はスキップされる

# ・NoSuchElementException：Selenium が要素を見つけられなかったときに投げる、例外クラスの名前
# find_element(...) が失敗すると、この例外が発生

# ・as e

# 発生した例外オブジェクトを、e という変数に入れて受け取る。以降の行で e を使って、例外の種類名やメッセージを参照できる

# まとめると：
# 「try の中で NoSuchElementException が発生したら、それを e という名前で受け取り、このブロックで処理する」 という宣言


#             print(f"[ERROR] 要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")

# e.__class__	：e（エラーオブジェクト）がどのクラス（設計図）から作られたかという情報を取り出す

# e.__class__.__name__	：そのクラスの正式名称（文字列）を取り出す
# 例：NoSuchElementException、TimeoutException、ValueError など⇒ 「どんな種類の例外だったのか（名前）」 を文字列で表示できる
# {e}	：エラーオブジェクトeを文字列に変換し、エラーの具体的なメッセージ（例：「Unable to locate element...」）を出力する

# 出力イメージ
# [ERROR] 要素取得失敗
# By=name
# Value=q_not_found
# NoSuchElementException:
# Message: no such element: Unable to locate element: {"method":"css selector","selector":"[name="q_not_found"]"}
# こうして レベル（ERROR）・探し方・値・例外名・詳細メッセージ が一目で分かるログになる

#             raise 

# raise は、捕まえた例外をそのまま上の呼び出し元へ投げ直す命令（再スロー）
# もし raise がないと、エラーが発生しても何も起こらず、
# プログラムは「要素を見つけられたフリ」をして次の処理に進んでしまう。予期せぬバグが起きるので入れる。

#         except Exception as e:

# except NoSuchElementException as e: は「要素が見つからない」という特定の失敗だけを捕まえログを記録する
# それに対し、except Exception as e: は、それ以外のネットワークエラーや内部エラーなど
# あらゆる予期せぬ失敗を捕まえるための最後の安全網として機能する

#             print(f"[ERROR] 想定外、要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
#             raise 


#     def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:

# get_by_idという「要素をID属性で探す」メソッドを定義。
# selfはクラス自身を指すお約束の引数（インスタンスにアクセスできる）
# chrome: WebDriver	　Chromeウィンドウ＝ブラウザ操作用オブジェクト（WebDriver）を受け取る
# value: str	検索したいIDの具体的な値（例: "login_button"）を文字列で受け取る
# -> WebElement	　処理の結果、見つけた要素（WebElement）を呼び出し元に戻す

#             elem: WebElement =  self._find(chrome, By.ID, value)

#このクラスの共通検索メソッド (_find) を呼び出し、IDと値を使って要素を検索する処理を依頼している
# 結果、見つかった要素を、elem: WebElementという型ヒント付きの変数に代入

# return elem

# 代入された変数 elem に格納されている要素オブジェクトを、この get_by_id メソッドの呼び出し元に返却
# 代入した elem を呼び出し元に返すことで、呼び出し側から click() や send_keys() などの操作ができるようになる

# 麻生さんからの補足
# 基本、変数に入れてreturnするようにしましょう！
# 結果何が入ってるのかが明確になるように！

#第一引数に 'By.ID' を渡すのがポイント！
#    ex) elem = chrome.find_element(By.ID, "username")
# 「value のままでいい？」の答え
# 	•	OKなケース：呼び出し側で value = "username" のように中身が入っている／関数の引数として "username" が渡ってきて中身が入っている。
# 	•	NGなケース：value が未定義／空文字 ""／違う属性の値（id で探してるのに name の値を入れてしまう など）。
# 変数名が value でも locator_value でも何でも構いません。中身が正しいかが勝負です。



#     def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
#             elem: WebElement =  self._find(chrome, By.NAME, value)
#             return elem

# get_by_nameという「要素をNAME属性で探す」メソッドを定義
# Webページ上のすべての要素をチェック、指定された値と name="値" が完全に一致する要素を検索　ex)「name=‘login’」
# 最初に見つけた1つを WebElement として返す
# 主に入力欄やラジオボタンなど、ユーザーが入力したデータを識別するために使われる要素を探すときに非常に有効
# 同じnameが複数あるときは最初の1件しか取れない点に注意。


#     def get_by_css(self, chrome: WebDriver, value: str) -> WebElement:
#             elem: WebElement = self._find(chrome, By.CSS_SELECTOR, value)
#             return elem
# get_by_cssという「要素をCSSセレクタ属性で探す」メソッドを定義
# CSSセレクタは、Webページの要素を正確に特定するための住所のようなルール言語。
# 主にHTMLのクラス名（.）やID名（#）、タグ名などを手がかりに要素を探す。idは「#id名」、nameは「[name='値']」のように書く。
# IDや名前がない場合でも、CSSセレクタはタグ名・class・属性を自由に組み合わせられる。親子関係や要素の順番などの位置情報を使って特定できるのが強み。
# CSSセレクタは全部できるが、書き方がやや長くて複雑。迷ったら、まずID→NAME→CSSの順に試すのが定石。
# CSSセレクタは「複数条件」や「構造指定」が必要なときに真価を発揮。つまり、ID/NAMEは“速い道具”、CSSは“万能な道具”として使い分ける。
# By.ID や By.NAME = 「ピンポイント住所で探す」
# By.CSS_SELECTOR = 「条件を組み合わせて探す検索機能」
# （たとえば「スーパーの近くのコンビニ」みたいに柔軟に指定できる）


#     def get_by_xpath(self, chrome: WebDriver, value: str) -> WebElement:
#             elem: WebElement =  self._find(chrome, By.XPATH, value)
#             return elem
# get_by_xpathという「要素をXPath属性で探す」メソッドを定義
# XPathは、HTMLのツリー構造をたどって目的の要素を探す方法
# XPath = XML Path Language（エックス・パス・ランゲージ） の略
# もともとは「XML」という文書構造をたどるための言語だが、HTMLも似た構造なので、Webページ内の要素を“住所のように”たどることができる
# Webページ全体のHTML構造を「家族の家系図」や「町の地図」のように捉え、そこから目的の要素がどこに、どんな順番で存在するかを指定する

# 動作のイメージ：「住所」で探す
# IDやクラス名のような目印がない要素を探すときに、XPathは非常に役立つ。
# 検索の難易度が高く、他の方法（By.IDやBy.CSS_SELECTOR）が使えない場合の最終手段として利用を推奨

# 検索方法	例	動作のイメージ
# ID (By.ID)	「山田さんの家」	表札（ID）を見てピンポイントで訪問する
# XPath (By.XPATH)	「市役所から3番目の建物の、2階の、左から4番目の窓」	地図の階層構造をたどり、相対的な位置で訪問する

# XPathの記述例
# XPathの記述は独特で、HTMLの階層をスラッシュ（/）で区切って表現 
# スラッシュ（/）を使って親子関係を表現し、属性（@name='値'）を使って絞り込む
# メリット	デメリット
# 最も強力: IDやクラス名など、どんな目印がなくても要素を探し出すことができる	
# 壊れやすい: Webページのデザインや構造が少しでも変わると、XPathの道順がすぐに無効になってしまう

#     def get_by_class_name(self, chrome: WebDriver, value: str) -> WebElement:
#             elem: WebElement =  self._find(chrome, By.CLASS_NAME, value)
#             return elem
# get_by_class_nameという「要素をclass属性に書かれた値を使って探す」メソッドを定義
# 動作のイメージ：「グループ名」で探す
# Webサイトのボタンを例に考えてみる。属性　役割 動作のイメージ
# ID (By.ID)	個人名（ユニーク）	「山田さん一人だけ」を探す。
# CLASS (By.CLASS_NAME)	グループ名（共通）	「sale-item というグループ名を持つ全員」を探す。
# 特徴: 複数の要素に共通の目印（グループ名）として同じクラス名が設定されている場合に非常に有効。
# Webページ上で「同じ見た目・グループ」の要素をまとめて指定できる。
# 動作: 指定したクラス名と完全に一致する要素を、Webページ全体から探し出す。
# find_element は最初の1つだけ、find_elements は全部取れる。
# class名が複数ついている場合は、空白を入れずに1つだけ指定する。
# ボタンやフォーム、ラベルなどの共通デザインを探すのに最適。
# 注意点
# 一意性がない: 複数の要素に同じクラス名が付くため、意図せず間違った要素を取得してしまうリスク
# 複数のクラスに対応不可: class="a b c" のように複数のクラスがある場合、すべてを組み合わせて検索することはできない。
# デザイン変更に弱い: 主にデザイン目的で使われるため、見た目の変更でクラス名が変わると、テストコードの修正が必要になる。


#     def get_by_tag_name(self, chrome: WebDriver, value: str) -> WebElement:
#             elem: WebElement = self._find(chrome, By.TAG_NAME, value)
#             return elem
# get_by_tag_nameという「要素をタグの名前を使って探す」メソッドを定義
# By.TAG_NAME は、HTML要素に付けられている タグの名前（例: button、input、div、a など）を使って要素を探す方法

# 「特定の種類のタグを一括で処理したいとき」によく使う
# # 例：
# 	•	ページ内のすべてのリンクを取得したい → By.TAG_NAME, "a"
# 	•	すべての画像を取得したい → By.TAG_NAME, "img"
# 	•	すべてのテキスト入力欄を取得したい → By.TAG_NAME, "input"
# Webページのすべての部品は、それぞれの役割に応じて「タグ」という名前を持っている

# 動作のイメージ：「種類」でまとめて探す
# Webページの部品を、文房具に例える。
# 検索方法	動作のイメージ	HTMLタグの例
# ID (By.ID)	「特定のメーカー名と品番が書かれた鉛筆」を探す。	<input id="user-id">
# TAG_NAME (By.TAG_NAME)	「すべての『鉛筆』を種類でまとめて探す。」	<input>
# By.TAG_NAME は、ページ上の同じ種類の要素をすべて見つけ出すときに非常に便利。 
# 使い方
# By.TAG_NAME を使うと、Webページにそのタグ名を持つ要素が一つでも複数でも見つかる。
# 単数検索 (今回のコードの _find の場合): get_by_tag_name(chrome, "button") のように実行すると、
# Seleniumはページ上で最初に見つかった <button> 要素を一つだけ返す。
# 複数検索: find_elements(By.TAG_NAME, "a") のように使えば、ページ上のすべてのリンク要素（<a>タグ）をリストとして取得できる
# フォームの全入力欄やリンクをまとめて処理するときに便利。
# 注意点
# 同じタグ名はページにたくさんあることが多い。
# find_element は最初の1個だけ、find_elements は全部取る。
# タグ名は 英語の小文字 で指定するのがルール（例："INPUT"ではなく"input"


#     def get_by_link_text(self, chrome: WebDriver, value: str) -> WebElement:
#             elem: WebElement = self._find(chrome, By.LINK_TEXT, value)
#             return elem
# get_by_link_textという「Webページ上のリンク要素（<a>タグ）を探す」メソッドを定義
# By.LINK_TEXT とは？
# By.LINK_TEXT はリンク要素（<a>タグ）を画面上に表示されている文字列（リンクテキスト）と完全に一致させて探す方法
# たとえば、「お問い合わせ」と書かれたリンクを探すとき、裏側のIDやクラス名ではなく、「お問い合わせ」という目に見える文字をそのまま使って探す

# 動作のイメージ：「看板の文字」で探す
# ショッピングサイトのリンクを例に考えてみる
# 目的: Webページ上にある「商品を見る」というリンクをクリックしたい
# HTML（Webページの裏側）: リンク要素は <a href="/products">商品を見る</a> のように書かれている
# By.LINK_TEXT を使い、値として "商品を見る" を指定する
# Seleniumの動作: Seleniumはページ全体を探し、「<a>タグの中にある文字が『商品を見る』と完全に一致する要素」をピンポイントで見つけ出す

# 注意点
# 特徴: HTMLの裏側のIDやクラス名を知らなくても、目に見える文字さえ分かれば要素を特定できる。シンプルなリンククリックをしたいときに最適。
# 完全一致: リンクの文字（例: "詳細はこちら"）と、指定する値（例: "詳細はこちら"）が一文字一句すべて一致している必要がある。
# 対象: <a> タグ（ハイパーリンク）のみが対象。探せるのは <a> タグ（リンク）だけ。他のボタンや要素には使えない。
# この方法は、特にナビゲーションリンクなど、表示されているテキストが明確で変わらない要素を探す場合に最も分かりやすく直感的に使える検索方法
# 表示テキストが動的に変わるサイトでは不向き


#     def get_by_partial_link_text(self, chrome: WebDriver, value: str) -> WebElement:
#             elem: WebElement = self._find(chrome, By.PARTIAL_LINK_TEXT, value)
#             return elem
# get_by_partial_link_textという「Webページ上のリンク要素（<a>タグ）を探す(文字列の一部のみ)」メソッドを定義
# By.PARTIAL_LINK_TEXT はリンク文字を部分一致で探す方法。名前の「Partial（パーシャル）」は「部分的な」という意味
# リンク要素の表示されている文字列の一部が、指定した値と一致することを条件に探す。
# リンクテキストのすべてを知らなくても、特徴的な一部のキーワードだけで要素を特定できるのが強み
# 複数のリンクが同じ部分文字列を持っている場合、最初に見つかったリンクが返されるため、注意が必要
# テキストが長すぎるリンクや、一部が動的に変わるリンクを探す際に非常に便利
# <a> タグの中のテキストに、指定した文字が「含まれていれば」ヒットする。
# 例："ログイン" で:「ログインはこちら」「ログイン方法」も見つかる。
# 複数似た文字があるときは誤クリックに注意。「文字が少し変わるリンク」でも柔軟に対応できる。









# #chatGPTが出したコード

# from __future__ import annotations
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webdriver import WebDriver
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException, WebDriverException


# class GetElement:
#     """
#     要素取得専用クラス（学習用：printで前後ログを出す版）
#     ※ 今回は logger 未使用。のちに print を logger.debug/error に置換するだけで移行できる設計。
#     """

#     def __init__(self, chrome: WebDriver, logger=None) -> None:
#         # 要件：__init__(self, chrome, logger) で受け取るが、今回は print 学習版のため logger は保持のみ
#         self.chrome: WebDriver = chrome
#         self.logger = logger

#     # --- 内部共通関数：前後ログ＋例外処理を1か所に集約 ---
#     def _find(self, by: str, value: str) -> WebElement:
#         print(f"[DEBUG] 要素取得開始:\nBy={by}\nValue={value}")
#         try:
#             element: WebElement = self.chrome.find_element(by, value)
#             print(f"[DEBUG] 要素取得完了:\nBy={by}\nValue={value}")
#             return element
#         except (NoSuchElementException, WebDriverException) as e:
#             print(f"[ERROR] 要素取得失敗(既知例外):\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
#             raise
#         except Exception as e:
#             # 予期しない例外もログして必ず上に伝える
#             print(f"[ERROR] 要素取得失敗(想定外例外):\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
#             raise

#     # 以降は要件順で個別メソッドを定義（中身は共通関数に委譲）
#     def get_by_id(self, value: str) -> WebElement:
#         return self._find(By.ID, value)

#     def get_by_name(self, value: str) -> WebElement:
#         return self._find(By.NAME, value)

#     def get_by_css(self, value: str) -> WebElement:
#         return self._find(By.CSS_SELECTOR, value)

#     def get_by_xpath(self, value: str) -> WebElement:
#         return self._find(By.XPATH, value)

#     def get_by_class_name(self, value: str) -> WebElement:
#         return self._find(By.CLASS_NAME, value)

#     def get_by_tag_name(self, value: str) -> WebElement:
#         return self._find(By.TAG_NAME, value)

#     def get_by_link_text(self, value: str) -> WebElement:
#         return self._find(By.LINK_TEXT, value)

#     def get_by_partial_link_text(self, value: str) -> WebElement:
#         return self._find(By.PARTIAL_LINK_TEXT, value)
    
    
    
    
# #Geminiが出したコード 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webdriver import WebDriver
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException

# class GetElement:
#     def __init__(self, chrome: WebDriver):
#         self.chrome = chrome

#     def get_by_id(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.ID, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_name(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.NAME, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_css(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.CSS_SELECTOR, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_xpath(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.XPATH, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_class_name(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.CLASS_NAME, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_tag_name(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.TAG_NAME, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_link_text(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.LINK_TEXT, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e

#     def get_by_partial_link_text(self, value: str) -> WebElement:
#         try:
#             print(f"要素取得開始: \n{value}")
#             element = self.chrome.find_element(By.PARTIAL_LINK_TEXT, value)
#             print(f"要素取得完了: \n{value}")
#             return element
#         except NoSuchElementException as e:
#             print(f"要素取得失敗: \n{e}")
#             raise e