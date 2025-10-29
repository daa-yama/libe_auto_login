# GetElement1 行づつ解説

```py
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
```

<br>

---

```py
from selenium.webdriver.common.by import By
```

selenium の中にある webdriver 機能のうち common (共通) の仕組みから
`By` という　要素の検索方法を定義した設計図（クラス）を取り込んでいます

**（例：By.ID, By.NAME, By.CSS_SELECTOR, By.XPATH）**

```py
from selenium.webdriver.remote.webdriver import WebDriver
```

Selenium の中にある webdriver 機能のうち、remote (遠隔操作) をするための仕組みから
WebDriver というブラウザ操作の設計図（クラス）を取り込んでいます<br>
`remote` = ネットワーク越しのブラウザ操作を可能にするモジュール(遠隔操作)
webdriver は Web ブラウザを操作するインターフェース

```py
from selenium.webdriver.remote.webelement import WebElement
```

selenium の中にある webdriver 機能のうち remote リモートで動かす仕組みから WebElement というブラウザ上の要素（ボタンや入力欄など）を表す設計図（クラス）で、`find_element()` の結果として実際に返ってくるオブジェクトです

```py
from selenium.common.exceptions import NoSuchElementException
```

Selenium の中にある common (共通) の例外（エラー）の仕組みから、
`NoSuchElementException` という「要素が見つからなかった」というエラーの設計図（クラス）を取り込んでいます。
（要素が見つからないときに出るエラーをインポートしている）
`selenium.common.exceptions` は Selenium が用意している「エラーの種類（例外クラス）」がまとめられているモジュール。
その中の `NoSuchElementException` は「find_element で指定した要素が見つからないときに自動で投げられるエラー」。
これを `except NoSuchElementException:` で受け止めることで、エラーになって処理が止まるのを防ぎ、ログを出したりリトライしたりできる。

```py
 class GetElement:
```

```py
def _find(self, chrome:WebDriver, by: str, value: str) -> WebElement:
```

`＿find`という探すメソッドを定義。それぞれの引数 self はクラス自身、`chrome:Webdriver`はブラウザを操作するオブジェクト、
`by: str`で検索方法（By.ID や By.XPATH など）を文字列で受け取り、
`value: str`で検索する実際の値（ID 名や CSS セレクタなど　例: "username", "q"）を文字列で受け取る。それを WebElement に返している。
<br><br>・`str` = strings の略。文字列が入りますよという型ヒント。<br>・`-> 〇〇` = 〇〇を戻すという目印

```py
try:
```

要素の検索を試み、成功すれば要素を返却する
<br>ここから先の処理で失敗（例外）が起きるかもしれないので、「見張りモード」で実行する合図
<br>`try:` のブロック内でエラーが起きると、以降の行は実行されず、対応する `except` にジャンプ
<br>後続の `print` や `return` が実行されるのは成功した場合だけ

```py
 print(f"[DEBUG] 要素取得開始\nBy={by}\nValue={value}")
```

これから探しに行く条件を記録する「開始ログ」
<br>`\n `は改行。読みやすさの為
<br>将来的に 本番用に`print` を `logger.debug` に置き換える
<br>デバッグ時、「何を探しに行ったのか」がわかる

```py
elem = chrome.find_element(by, value)
```

WebDriver（chrome）に「`by` という探し方で、`value` という具体値を探せ」と命令
<br>• 例：`by=By.ID`, `value="username"` なら、`id="username"` の要素を探します。
<br>• 見つかれば、右辺の結果（WebElement オブジェクト）が左の `elem` に代入されます。
<br> • 見つからないときはここで例外（`NoSuchElementException` など）が発生し、下の行はスキップされて `except` に移動します。

```py
print(f"[DEBUG] 要素取得完了\nBy={by}\nValue={value}")
```

検索が成功した直後に出す「完了ログ」

```py
return elem
```

見つけた WebElement を呼び出し元へ返す行
<br>`return` に到達した時点で関数は終了
<br>その後の行は実行されない

```py
except  NoSuchElementException as e:
```

`try` ブロック内で、「探している要素が Web ページ上に存在しない」という特定の失敗（`NoSuchElementException`）が発生した場合に、
この処理を開始。
<br>発生したエラーオブジェクトを e という変数に代入

・`except: try`ブロックの中でエラー（例外）が起きた場合に、ここで受け止めて処理するためのキーワード　例外が起きなければこの行はスキップされる
<br>・`NoSuchElementException` selenium が要素を見つけられなかったときに投げる、例外クラスの名前
<br>・`find_element(...)` が失敗すると、この例外が発生
<br>
・`as e`
発生した例外オブジェクトを、`e` という変数に入れて受け取る。以降の行で `e` を使って、例外の種類名やメッセージを参照できる

**まとめると：**
<br>「`try` の中で `NoSuchElementException` が発生したら、それを `e` という名前で受け取り、このブロックで処理する」 という宣言

```py
print(f"[ERROR] 要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
```

`e.__class__`：`e`（エラーオブジェクト）がどのクラス（設計図）から作られたかという情報を取り出す

` e.__class__.__name__` ：そのクラスの正式名称（文字列）を取り出す
<br>例：NoSuchElementException、TimeoutException、ValueError など ⇒ 「どんな種類の例外だったのか（名前）」 を文字列で表示できる
<br> `{e}` ：エラーオブジェクト`e`を文字列に変換し、エラーの具体的なメッセージ（例：「Unable to locate element...」）を出力する

**出力イメージ**<br>

```py
 [ERROR] 要素取得失敗
 By=name
 Value=q_not_found
 NoSuchElementException:
 Message: no such element: Unable to locate element: {"method":"css selector","selector":"[name="q_not_found"]"}
```

こうして レベル（ERROR）・探し方・値・例外名・詳細メッセージ が一目で分かるログになる

```py
raise
```

`raise` は、捕まえた例外をそのまま上の呼び出し元へ投げ直す命令（再スロー）
もし `raise` がないと、エラーが発生しても何も起こらず、プログラムは「要素を見つけられたフリ」をして次の処理に進んでしまう。予期せぬバグが起きるので入れる。

```py
except Exception as e:
```

`except NoSuchElementException as e:` は「要素が見つからない」という特定の失敗だけを捕まえログを記録する
<br>それに対し、`except Exception as e:` は、それ以外のネットワークエラーや内部エラーなどあらゆる予期せぬ失敗を捕まえるための最後の安全網として機能する

```py
print(f"[ERROR] 想定外、要素取得失敗\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
 raise
```

---

```py
def get_by_id(self, chrome: WebDriver, value: str) -> WebElement:
```

`get_by_id`という　**「要素を ID 属性で探す」**　メソッドを定義。
<br>`self`はクラス自身を指すお約束の引数（インスタンスにアクセスできる）
<br>`chrome: WebDriver` 　 Chrome ウィンドウ＝ブラウザ操作用オブジェクト（WebDriver）を受け取る
<br>`value: str` 検索したい ID の具体的な値（例: "login_button"）を文字列で受け取る
<br>`-> WebElement` 　処理の結果、見つけた要素（WebElement）を呼び出し元に戻す

```py
elem: WebElement =  self._find(chrome, By.ID, value)
```

このクラスの共通検索メソッド (`_find`) を呼び出し、ID と値を使って要素を検索する処理を依頼している
<br>結果、見つかった要素を、`elem: WebElement`という型ヒント付きの変数に代入

```py
return elem
```

代入された変数 `elem` に格納されている要素オブジェクトを、この `get_by_id` メソッドの呼び出し元に返却
代入した elem を呼び出し元に返すことで、呼び出し側から `click()` や `send_keys()` などの操作ができるようになる

# 麻生さんからの補足

# 基本、変数に入れて return するようにしましょう！<br>結果何が入ってるのかが明確になるように！

第一引数に `'By.ID'` を渡すのがポイント！
<br> ` ex) elem = chrome.find_element(By.ID, "username")`
<br><br>**「value のままでいい？」の答え**<br>
• OK なケース：呼び出し側で value = "username" のように中身が入っている／関数の引数として "username" が渡ってきて中身が入っている。
<br><br>• NG なケース：value が未定義／空文字 ""／違う属性の値（id で探してるのに name の値を入れてしまう など）。
<br><br>変数名が value でも locator_value でも何でも構いません。中身が正しいかが勝負です。

```py
def get_by_name(self, chrome: WebDriver, value: str) -> WebElement:
elem: WebElement =  self._find(chrome, By.NAME, value)
return elem
```

・`get_by_name`という **「要素を NAME 属性で探す」** メソッドを定義
<br>・Web ページ上のすべての要素をチェック、指定された値と name="値" が完全に一致する要素を検索　 ex)「name=‘login’」
<br>・最初に見つけた 1 つを WebElement として返す
<br>・主に入力欄やラジオボタンなど、ユーザーが入力したデータを識別するために使われる要素を探すときに非常に有効
<br>・同じ name が複数あるときは最初の 1 件しか取れない点に注意。

```py
def get_by_css(self, chrome: WebDriver, value: str) -> WebElement:
elem: WebElement = self._find(chrome, By.CSS_SELECTOR, value)
return elem
```

・`get_by_css`という **「要素を CSS セレクタ属性で探す」** メソッドを定義
<br>・CSS セレクタは、Web ページの要素を正確に特定するための住所のようなルール言語。
<br>・主に HTML のクラス名（.）や ID 名（#）、タグ名などを手がかりに要素を探す。id は「#id 名」、name は「[name='値']」のように書く。
<br>・ID や名前がない場合でも、CSS セレクタはタグ名・class・属性を自由に組み合わせられる。親子関係や要素の順番などの位置情報を使って特定できるのが強み。
<br>・CSS セレクタは全部できるが、書き方がやや長くて複雑。迷ったら、まず ID→NAME→CSS の順に試すのが定石。
<br>・CSS セレクタは「複数条件」や「構造指定」が必要なときに真価を発揮。つまり、ID/NAME は“速い道具”、CSS は“万能な道具”として使い分ける。
<br>・By.ID や By.NAME = **「ピンポイント住所で探す」**
<br>・By.CSS_SELECTOR = **「条件を組み合わせて探す検索機能」**
<br>（たとえば「スーパーの近くのコンビニ」みたいに柔軟に指定できる）

```py
def get_by_xpath(self, chrome: WebDriver, value: str) -> WebElement:
elem: WebElement =  self._find(chrome, By.XPATH, value)
return elem
```

・`get_by_xpath`という **「要素を XPath 属性で探す」** メソッドを定義
<br>・XPath は、HTML のツリー構造をたどって目的の要素を探す方法
<br>・XPath = XML Path Language（エックス・パス・ランゲージ） の略
<br>・元々は「XML」という文書構造をたどるための言語だが、HTML も似た構造なので、Web ページ内の要素を“住所のように”たどることができる
<br>・web ページ全体の HTML 構造を「家族の家系図」や「町の地図」のように捉え、そこから目的の要素がどこに、どんな順番で存在するかを指定する
<br><br>**動作のイメージ：「住所」で探す**
<br>ID やクラス名のような目印がない要素を探すときに、XPath は非常に役立つ。
<br>検索の難易度が高く、他の方法（By.ID や By.CSS_SELECTOR）が使えない場合の最終手段として利用を推奨

<br>**検索方法 例)動作のイメージ**
<br>ID (By.ID) 「山田さんの家」 表札（ID）を見てピンポイントで訪問する
<br><br>XPath (By.XPATH) 「市役所から 3 番目の建物の、2 階の、左から 4 番目の窓」 地図の階層構造をたどり、相対的な位置で訪問する

**XPath の記述例**
<br>・XPath の記述は独特で、HTML の階層をスラッシュ（/）で区切って表現
<br>・スラッシュ（/）を使って親子関係を表現し、属性（@name='値'）を使って絞り込む
<br>**メリット デメリット**
<br>最も強力: ID やクラス名など、どんな目印がなくても要素を探し出すことができる
<br>壊れやすい: Web ページのデザインや構造が少しでも変わると、XPath の道順がすぐに無効になってしまう

```py
def get_by_class_name(self, chrome: WebDriver, value: str) -> WebElement:
elem: WebElement =  self._find(chrome, By.CLASS_NAME, value)
return elem
```

`get_by_class_name`という **「要素を class 属性に書かれた値を使って探す」** メソッドを定義
<br>**動作のイメージ：「グループ名」で探す**
<br><br>Web サイトのボタンを例に考えてみる。属性 役割 動作のイメージ
<br>・`ID (By.ID)` 個人名（ユニーク） 「山田さん一人だけ」を探す。
<br>・`CLASS (By.CLASS_NAME)` グループ名（共通） 「sale-item というグループ名を持つ全員」を探す。
<br><br>・特徴: 複数の要素に共通の目印（グループ名）として同じクラス名が設定されている場合に非常に有効。
<br>・Web ページ上で「同じ見た目・グループ」の要素をまとめて指定できる。
<br>・動作: 指定したクラス名と完全に一致する要素を、Web ページ全体から探し出す。
<br>・`find_element` は最初の 1 つだけ、`find_elements` は全部取れる。
<br>・class 名が複数ついている場合は、空白を入れずに 1 つだけ指定する。
<br>・ボタンやフォーム、ラベルなどの共通デザインを探すのに最適。
<br><br>**注意点**

---

・一意性がない: 複数の要素に同じクラス名が付くため、意図せず間違った要素を取得してしまうリスク
<br>・複数のクラスに対応不可: class="a b c" のように複数のクラスがある場合、すべてを組み合わせて検索することはできない。
<br>・デザイン変更に弱い: 主にデザイン目的で使われるため、見た目の変更でクラス名が変わると、テストコードの修正が必要になる。

```py
def get_by_tag_name(self, chrome: WebDriver, value: str) -> WebElement:
elem: WebElement = self._find(chrome, By.TAG_NAME, value)
return elem
```

・`get_by_tag_name`という **「要素をタグの名前を使って探す」** メソッドを定義
<br>・By.TAG_NAME は、HTML 要素に付けられている タグの名前（例: button、input、div、a など）を使って要素を探す方法
<br>・「特定の種類のタグを一括で処理したいとき」によく使う
<br><br> 例：
<br>• ページ内のすべてのリンクを取得したい → By.TAG_NAME, "a"
<br> • すべての画像を取得したい → By.TAG_NAME, "img"
<br>• すべてのテキスト入力欄を取得したい → By.TAG_NAME, "input"
<br><br>・Web ページのすべての部品は、それぞれの役割に応じて「タグ」という名前を持っている

<br>**動作のイメージ：「種類」でまとめて探す**
<br>・Web ページの部品を、文房具に例える。
<br>・検索方法 動作のイメージ HTML タグの例
<br>**ID (By.ID)**
<br>「特定のメーカー名と品番が書かれた鉛筆」を探す。

```html
<input id="user-id" />
```

**TAG_NAME (By.TAG_NAME)**
<br> 「すべての『鉛筆』を種類でまとめて探す。」

```html
<input />
```

`By.TAG_NAME` は、ページ上の同じ種類の要素をすべて見つけ出すときに非常に便利。
<br><br> **使い方**
<br>`By.TAG_NAME` を使うと、Web ページにそのタグ名を持つ要素が一つでも複数でも見つかる。
<br><br>単数検索 (今回のコードの `_find` の場合): `get_by_tag_name(chrome, "button")` のように実行すると、
Selenium はページ上で最初に見つかった `<button>` 要素を一つだけ返す。
<br><br>複数検索: `find_elements(By.TAG_NAME, "a")` のように使えば、ページ上のすべてのリンク要素（`<a>`タグ）をリストとして取得できる
<br>フォームの全入力欄やリンクをまとめて処理するときに便利。
<br><br>**注意点**

---

<br>・同じタグ名はページにたくさんあることが多い。
<br>・`find_element` は最初の 1 個だけ、`find_elements` は全部取る。
<br>・タグ名は 英語の小文字 で指定するのがルール（例："INPUT"ではなく"input")

```py
def get_by_link_text(self, chrome: WebDriver, value: str) -> WebElement:
elem: WebElement = self._find(chrome, By.LINK_TEXT, value)
return elem
```

・`get_by_link_text`という **「Web ページ上のリンク要素（`<a>`タグ）を探す」** メソッドを定義
<br><br>**By.LINK_TEXT とは？**
<br>`By.LINK_TEXT` はリンク要素（`<a>`タグ）を画面上に表示されている文字列（リンクテキスト）と完全に一致させて探す方法
<br>例えば、「お問い合わせ」と書かれたリンクを探すとき、裏側の ID やクラス名ではなく、「お問い合わせ」という目に見える文字をそのまま使って探す
<br><br> **動作のイメージ：「看板の文字」で探す**
<br>ショッピングサイトのリンクを例に考えてみる
<br>**目的: Web ページ上にある「商品を見る」というリンクをクリックしたい**

---

HTML（Web ページの裏側）: リンク要素は
`<a href="/products">商品を見る</a>` のように書かれている
By.LINK_TEXT を使い、値として "商品を見る" を指定する
<br>Selenium の動作: Selenium はページ全体を探し、「`<a>`タグの中にある文字が『商品を見る』と完全に一致する要素」をピンポイントで見つけ出す

<br>**注意点**

---

・特徴: HTML の裏側の ID やクラス名を知らなくても、目に見える文字さえ分かれば要素を特定できる。シンプルなリンククリックをしたいときに最適。
<br>・完全一致: リンクの文字（例: "詳細はこちら"）と、指定する値（例: "詳細はこちら"）が一文字一句すべて一致している必要がある。
<br>・対象: `<a>` タグ（ハイパーリンク）のみが対象。探せるのは `<a>` タグ（リンク）だけ。他のボタンや要素には使えない。
<br>・この方法は、特にナビゲーションリンクなど、表示されているテキストが明確で変わらない要素を探す場合に最も分かりやすく直感的に使える検索方法
<br>・表示テキストが動的に変わるサイトでは不向き

```py
def get_by_partial_link_text(self, chrome: WebDriver, value: str) -> WebElement:
elem: WebElement = self._find(chrome, By.PARTIAL_LINK_TEXT, value)
return elem
```

・`get_by_partial_link_text`という **「Web ページ上のリンク要素（`<a>`タグ）を探す(文字列の一部のみ)」** メソッドを定義
<br>・`By.PARTIAL_LINK_TEXT` はリンク文字を部分一致で探す方法。名前の「Partial（パーシャル）」は「部分的な」という意味
<br>・リンク要素の表示されている文字列の一部が、指定した値と一致することを条件に探す。
<br>・リンクテキストのすべてを知らなくても、特徴的な一部のキーワードだけで要素を特定できるのが強み
<br>・複数のリンクが同じ部分文字列を持っている場合、最初に見つかったリンクが返されるため、注意が必要
<br>・テキストが長すぎるリンクや、一部が動的に変わるリンクを探す際に非常に便利
<br>・`<a>` タグの中のテキストに、指定した文字が「含まれていれば」ヒットする。
<br>・例："ログイン" で:「ログインはこちら」「ログイン方法」も見つかる。
<br>・複数似た文字があるときは誤クリックに注意。「文字が少し変わるリンク」でも柔軟に対応できる。

## 🧩 1 行まとめ

| 方法                     | 探す基準               | 特徴                                                                                 |
| ------------------------ | ---------------------- | ------------------------------------------------------------------------------------ |
| **By.ID**                | `id` 属性              | 一番速くてシンプル（ただし id がないと使えない）                                     |
| **By.NAME**              | `name` 属性            | 主にフォーム入力欄で使う                                                             |
| **By.LINK_TEXT**         | リンク文字（完全一致） | 「クリックできるテキスト」がピッタリ一致するリンクを探す。安全で確実。               |
| **By.PARTIAL_LINK_TEXT** | リンク文字（部分一致） | 一部の文字を含むリンクを探せる。柔軟だが誤検出に注意。                               |
| **By.CSS_SELECTOR**      | CSS セレクタ           | ID・クラス・タグなどを組み合わせて細かく指定可能。最も自由度が高い。                 |
| **By.TAG_NAME**          | HTML タグ名            | 例：`div`, `a`, `input` などのタグ種類で要素を探す。構造確認や全取得に便利。         |
| **By.CLASS_NAME**        | `class` 属性           | デザインやレイアウト用のクラスを指定して要素を探す。複数要素に共通して使われやすい。 |
| **By.XPATH**             | HTML の構造（パス）    | id や name がなくても、「階層構造」「位置」「テキスト」などで柔軟に探せる。          |

## chatGPT が出したコード

```py
from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, WebDriverException

class GetElement:
"""
要素取得専用クラス（学習用：printで前後ログを出す版）
※ 今回は logger 未使用。のちに print を logger.debug/error に置換するだけで移行できる設計。
#     """

    def __init__(self, chrome: WebDriver, logger=None) -> None:
        # 要件：__init__(self, chrome, logger) で受け取るが、今回は print 学習版のため logger は保持のみ
        self.chrome: WebDriver = chrome
        self.logger = logger

    # --- 内部共通関数：前後ログ＋例外処理を1か所に集約 ---
    def _find(self, by: str, value: str) -> WebElement:
        print(f"[DEBUG] 要素取得開始:\nBy={by}\nValue={value}")
        try:
            element: WebElement = self.chrome.find_element(by, value)
            print(f"[DEBUG] 要素取得完了:\nBy={by}\nValue={value}")
            return element
        except (NoSuchElementException, WebDriverException) as e:
            print(f"[ERROR] 要素取得失敗(既知例外):\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
            raise
        except Exception as e:
            # 予期しない例外もログして必ず上に伝える
            print(f"[ERROR] 要素取得失敗(想定外例外):\nBy={by}\nValue={value}\n{e.__class__.__name__}: {e}")
            raise

    # 以降は要件順で個別メソッドを定義（中身は共通関数に委譲）
    def get_by_id(self, value: str) -> WebElement:
        return self._find(By.ID, value)

    def get_by_name(self, value: str) -> WebElement:
        return self._find(By.NAME, value)

    def get_by_css(self, value: str) -> WebElement:
        return self._find(By.CSS_SELECTOR, value)

    def get_by_xpath(self, value: str) -> WebElement:
        return self._find(By.XPATH, value)

     def get_by_class_name(self, value: str) -> WebElement:
         return self._find(By.CLASS_NAME, value)

     def get_by_tag_name(self, value: str) -> WebElement:
         return self._find(By.TAG_NAME, value)

     def get_by_link_text(self, value: str) -> WebElement:
         return self._find(By.LINK_TEXT, value)

 def get_by_partial_link_text(self, value: str) -> WebElement:
     return self._find(By.PARTIAL_LINK_TEXT, value)
```

## Gemini が出したコード

```py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

class GetElement:
    def __init__(self, chrome: WebDriver):
        self.chrome = chrome

    def get_by_id(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.ID, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e

    def get_by_name(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.NAME, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e

    def get_by_css(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.CSS_SELECTOR, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e

    def get_by_xpath(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.XPATH, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e

    def get_by_class_name(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.CLASS_NAME, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e

    def get_by_tag_name(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.TAG_NAME, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e

    def get_by_link_text(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.LINK_TEXT, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e

    def get_by_partial_link_text(self, value: str) -> WebElement:
        try:
            print(f"要素取得開始: \n{value}")
            element = self.chrome.find_element(By.PARTIAL_LINK_TEXT, value)
            print(f"要素取得完了: \n{value}")
            return element
        except NoSuchElementException as e:
            print(f"要素取得失敗: \n{e}")
            raise e
```

<br>
<br><br><br>

# ActionElement1 行づつ解説

```py
class ActionElement:
    """（print版）"""

    def __init__(self) -> None:
        pass

    def send_keys(self, element: WebElement, text: str) -> None:
        try:
            print("入力開始")
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def click(self, element: WebElement) -> None:
        try:
            print("クリック開始")
            element.click()
            print("クリック完了")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def clear_and_send_keys(self, element: WebElement, text: str) -> None:
        try:
            print("入力クリア＆開始")
            element.clear()
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise

    def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
        print("クリック開始")
        try:
                element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
                print(f"通常クリック不可（エラー種別: {type(e).__name__}）→ JavaScriptクリックでフォールバック")
        try:
                chrome.execute_script("arguments[0].click();", element)
        except Exception as js_e:
                print(f"JavaScriptクリックも失敗: {js_e}")
                raise
        except Exception as e:
                print(f"操作失敗: {e}")
                raise
        print("クリック完了")

    if __name__ == "__main__":
    chrome: WebDriver = webdriver.Chrome()
    try:
        chrome.get("https://libecity.com/signin")

        ge = GetElement()
        action = ActionElement()

        id_input = ge.get_by_css(chrome, "input[type='text']")
        action.clear_and_send_keys(id_input, "test@example.com")

        password_input = ge.get_by_css(chrome, "input[type='password']")
        action.clear_and_send_keys(password_input, "test1234")

        login_btn = ge.get_by_css(chrome, "button[type='submit']")
        action.safe_click(login_btn, chrome)

        time.sleep(3)
        print(chrome.current_url)
    finally:
        chrome.quit()
```

<br><br>

---

```py
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
```

NoSuchElementException は「**要素を見つけられない**」問題、後の二つは「**要素は見つけたが操作できない**」問題。
<br>
クリックを試したとき、別の要素に遮られると `ElementClickInterceptedException`、
<br>要素が非表示や無効状態だと `ElementNotInteractableException` になる。
<be>どちらも Selenium が要素の「通常クリックができない」という共通点があるので、同じ except 節で拾って JS クリックに切り替え。

```py
import time
```

`import time` は「Python の標準ライブラリ time モジュールを使うための宣言」<br>
そのモジュールの中にある time.sleep(秒数) という関数を使うことで、プログラムの実行を一時的に止める（待機する） ことができる。

```py
class ActionElement:
    """（print版）"""
```

```py
    def __init__(self) -> None:
        pass
```

このクラスには今のところ初期化すべき変数がないので、
初期化メソッド` __init__` は形式的に定義だけしておく。
<br>何も処理しないようにするため `pass` を入れている。
<br>戻り値は何も返さない（`None`）

```py
    def send_keys(self, element: WebElement, text: str) -> None:
        try:
            print("入力開始")
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise
```

`send_keys()`は指定された Web 要素に文字列を入力し、成功・失敗のログを出す安全な入力関数

```py
def send_keys(self, element: WebElement, text: str) -> None:
```

• クラス内でメソッド（関数）を定義している行<br>
• `self` はこのクラス自身を指す。クラスのメソッドには必ず最初の引数として書く。<br>
• `element` は「どの HTML 要素に対して操作を行うか」を表し、Selenium の WebElement 型であることを明示している。<br>
• `text` はその要素に送る文字列データ（例：「test@example.com」など）<br>
• `-> None` は「この関数は値を返さない」ことを型ヒントで示している。

```py
    try:
    print("入力開始")
    element.send_keys(text)
    print(f"入力完了: {text}")
```

• `try:` は「この中の処理を実行し、もし途中で例外（エラー）が起きたら `except` に移動する」という構文<br>
• `print("入力開始")` はユーザーに「これから文字入力を始めるよ」と知らせるログ出力<br>
• `element.send_keys(text)` は Selenium のコマンド で、実際に Web ページのテキストボックスなどに文字を入力する。<br>
→ たとえば「メールアドレス入力欄」に「test@example.com」を送ると実際にその欄に文字が入力される<br>
• `print(f"入力完了: {text}")` は f 文字列（フォーマット文字列）で、入力した内容をログに出している

```py
except Exception as e:
    print(f"操作失敗: {e}")
    raise
```

• `except` は「`try`ブロック内で何かエラーが起きた時」に動く部分<br>
• `Exception as e `は、発生したエラーを e という名前で受け取る<br>
• `print(f"操作失敗: {e}")` は、どんなエラーが起きたかをターミナルに表示<br>
たとえば「要素が見つからない」「入力できない」といった原因をログで確認できるようにしている<br>
• `raise` は「このエラーを上位に伝える（再送する）」命令で、
呼び出し元（例：main 側）にもこの失敗を通知して、処理を止めたり別の対処をさせたりできる

```py
    def click(self, element: WebElement) -> None:
        try:
            print("クリック開始")
            element.click()
            print("クリック完了")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise
```

`click()` は「指定された Web 要素をクリックし、その成功・失敗をログ出力するメソッド」<br>

```py
    def clear_and_send_keys(self, element: WebElement, text: str) -> None:
        try:
            print("入力クリア＆開始")
            element.clear()
            element.send_keys(text)
            print(f"入力完了: {text}")
        except Exception as e:
            print(f"操作失敗: {e}")
            raise
```

`clear_and_send_keys() `は、指定した Web 要素の入力欄をいったんクリアしてから新しい文字列を入力するためのメソッド<br>
・` element.clear()`
• Selenium の `clear()` メソッドを使って、入力欄の中にすでに入っている文字を削除。<br>
• これにより、古い値が残ったまま上書きされるミスを防ぐことができる。<br>
• たとえば、メールアドレス欄に "abc" が残っている状態で "xyz" を送ると "abcxyz" になってしまうため、
この `clear()` が先に実行されることが非常に重要になる。<br>
• Web フォームのテストやデータ入力では、この「クリアしてから入力」が基本パターン<br>

`element.send_keys(text)`<br>
• ここで実際に入力処理を行う。<br>
• `send_keys()` は Selenium のメソッドで、ブラウザに「キーボードで入力する動作」を指示する。<br>
• ここでは引数 `text` に渡された文字列（例：`test@example.com`）をフォームに入力。<br>
• `clear()` で消したあとにこの行を実行することで、常に新しい値を確実に入力できる。

```py
    def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
        print("クリック開始")
        try:
                element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
                print(f"通常クリック不可（エラー種別: {type(e).__name__}）→ JavaScriptクリックでフォールバック")
        try:
                chrome.execute_script("arguments[0].click();", element)
        except Exception as js_e:
                print(f"JavaScriptクリックも失敗: {js_e}")
                raise
        except Exception as e:
                print(f"操作失敗: {e}")
                raise
        print("クリック完了")
```

`safe_click()` は、「まず通常クリックを試し、失敗した場合に JavaScript クリックでフォールバックする安全なクリックメソッド」。<br>通常クリックができない場合の保険処理（フォールバック） を行うのが特徴。<br>
これにより、要素が重なっていたり非活性でもクリック処理を成功させやすくなる。

```py
def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
```

• ここでは「安全にクリックを行う」メソッドを定義しています。<br>
• `safe_click` の “safe” は「安全に」という意味で、通常クリックができない場合の保険処理（フォールバック） を行うのが特徴。<br>
• `element` はクリック対象の HTML 要素（例：ログインボタン）<br>
• `chrome` はブラウザ（`WebDriver`）そのもの。<br>
• `-> None` は「戻り値を返さない（クリックするだけの処理）」ことを示している。

```py
element.click()
```

• Selenium が提供する通常のクリックメソッド<br>
• ブラウザの中で実際に「その要素をマウスクリックする」動作をシミュレート<br>
• ただし、要素が画面外にあったり、別の要素で覆われていると、ここで例外が発生する<br>
• 特に `ElementClickInterceptedException` や `ElementNotInteractableException` が代表的な例

```py
except (ElementClickInterceptedException, ElementNotInteractableException) as e:
```

• 通常クリックがうまくいかないときに呼ばれる「特別なエラー処理部分」<br>
• 2 種類の例外をまとめて捕まえている：<br>
• `ElementClickInterceptedException`：要素が別の要素に重なっていてクリックできない<br>
• `ElementNotInteractableException`：要素が非活性（クリック無効）で操作できない<br>
• `as e` により、どちらのエラーが出たのかを `e`という変数で扱えるようにしている<br>
• つまり「クリックできなかった理由」をログで出す準備をしている。

```py
print(f"通常クリック不可（エラー種別: {type(e).__name__}）→ JavaScriptクリックでフォールバック")
```

• 通常クリックができなかった場合に、どの種類のエラーが発生したのかを出力<br>
• `type(e).__name__` は発生した例外のクラス名<br>
（例：`ElementNotInteractableException`）を文字列で取得する方法<br>
•「フォールバック」とは「代替手段を使う」という意味<br>
• ここでは、クリックできないときの代替として JavaScript によるクリック に切り替える。<br>

### 「通常クリック不可」

• これは「`element.click()` がうまくいかなかった」という意味<br>
• 例えば、ボタンが画面外にあって押せなかったり、ポップアップで隠れていたりする状態。そのような際にこのメッセージが出る。

### `type(e)._name_`

• `e` は「例外（エラーの情報）」が入っている変数<br>
• `type(e)` で「そのエラーがどんな型（クラス）なのか」を取り出す。<br>
• `. __name__` で「そのクラスの名前（＝エラーの名前）」を文字列として取得。つまり、「どんな種類のエラーか」を動的に取得してログに出している。<br>
・`ElementNotInteractableException` → 要素が非活性（クリックできない）<br>
・`ElementClickInterceptedException` → 他の要素が重なってクリックを妨げている

### 「→ JavaScript クリックでフォールバック」

• 「フォールバック」とは「失敗したときに代替手段に切り替える」こと<br>
• 普通の `.click()` がダメだったから、今度は JavaScript を使って無理やりクリックする作戦に切り替える、という宣言<br>
• ここは「自動化スクリプトの安全装置」のようなもの

#### 💬 イメージで言うと…

🚗 通常のクリック＝ブレーキペダルを普通に踏む<br>
⚠️ フォールバック＝ブレーキが効かないときに「サイドブレーキで止める」<br>

**このログ出力は「今、通常のブレーキ（クリック）が効かなかった！だからサイドブレーキ（JS クリック）に切り替えるよ！」という報告**

```py
 try:
```

• JavaScript クリック自体もエラーになる可能性があるため、ここでも `try` を使って安全に囲っている。<br>
• たとえばページがすでに遷移しかけていたり、DOM（ページ構造）が変わった瞬間にクリックしようとしたときに失敗する可能性がある。<br>
• そのため「通常クリック」と「JS クリック」は別々の try-except で分けて扱うのが良い習慣

```py
chrome.execute_script("arguments[0].click();", element)
```

• Selenium の `execute_script()` メソッドで、JavaScript コードを直接実行<br>
• "`arguments[0].click();`" というのは「渡された要素を JavaScript でクリックする」という命令<br>
• `element` は第 2 引数で `arguments[0]` に入るので、この 1 行で「JS 経由でクリック」が実行される。<br>
• これにより、通常の `.click()` ではクリックできなかった要素でも、強制的にクリックできるケースがある。

#### 🔍 何をしているか（ざっくり）

Selenium の `.click()` ではなく、JavaScript を直接ブラウザに実行させてクリックさせる方法<br>
つまり、「Selenium 経由で押す」ではなく、「ブラウザ自身に命令を出して押させる」動き

#### 💡 詳しく噛み砕くと

### `chrome.execute_script(...)`

• Selenium の `execute_script()` は「ブラウザ上で JavaScript を直接実行できる」関数<br>
• chrome（または driver）は WebDriver オブジェクトで、Python から Chrome を操作している。<br>
• これを使うと、ブラウザ内部の JavaScript の世界に命令を送ることができる。

### `"arguments[0].click();"`

• この部分が実際にブラウザに渡される JavaScript コード<br>
• `arguments[0]` は、「Python 側から渡された最初の引数」を指します（ここでは `element`）<br>
• つまり、Selenium で取得したボタン要素を`「arguments[0]」`として JS に渡して、
その要素に対して `.click()` を実行しています。

### element がどこに渡るか

• `execute_script` の第 2 引数に `element` を渡しているので、
JavaScript の中では `arguments[0]` が `element` に置き換えられる。<br>
• 結果として、ブラウザ内でこう動く 👇<br>
`element.click();  //` ← JavaScript レベルでクリック命令を実行<br>

### なぜこれで「強制クリック」ができるのか？

• JavaScript レベルで直接クリックイベントを発火させるため、
「画面外」「重なり」「非表示」などの制約をある程度無視してクリックできる。
• つまり、普通の Selenium `.click()` では届かない要素にも“裏口”からアクセスできるということ。

### ただし万能ではない！

• JavaScript でクリックしても、サイト側が JS イベントを無効化している場合は反応しないことがある。<br>
• そのため、「**どうしてもクリックできないときの最後の手段**」として使う。<br>
• これを組み合わせているからこそ「`safe_click`（安全クリック）」という名前になっている。

#### 💬 イメージで言うと…

🚪 `.click()` ＝ 正面玄関からドアをノックして入る<br>
🔑 `execute_script()` ＝ ドアが開かないときに、合鍵で裏口から入る<br>

#### どちらも「目的の部屋（ボタン）」にたどり着くけれど、方法が違う。裏口（JS クリック）は強引だが、確実に中に入れるというわけ。

```py
except Exception as js_e:
```

• JS クリック中に発生する想定外のエラーをここでキャッチ<br>
• ページが既にリロードされていたり、クリック対象が削除されている場合などに発生<br>
• `js_e` にはエラーの詳細が入るため、ログ出力で問題の原因を特定できる。

```py
print(f"JavaScriptクリックも失敗: {js_e}")
```

• JS クリックに失敗した場合に、どんな理由でうまくいかなかったのかを出力<br>
• `js_e` には実際のエラーメッセージ（例：stale element reference）が入るため、後からデバッグできる。<br>
• このログが出たら「通常クリックも JS クリックも失敗した」という意味

```py
raise
```

• この `raise` によって、JS クリックで発生したエラーを呼び出し元に伝える。<br>
• これにより、上位コードで「`safe_click` が失敗した」ことを検知できる。<br>
• エラーを隠さずに伝えることで、より堅牢な構造に。

```py
except Exception as e:
```

• これは「通常クリックでもなく、想定していない別のエラー」が発生したときに通る部分<br>
• 例えば、`NoSuchElementException`（要素が存在しない）や、`TimeoutException`（タイムアウト）など<br>
• つまり「クリックできない系」以外のあらゆる例外をここで拾って出力している。

```py
print(f"操作失敗: {e}")
```

• 想定外のエラーが出た場合、その詳細をログに残す。<br>
• これにより、原因をあとで追跡することができる。<br>
• たとえば「ボタンがまだロードされていなかった」などの問題もここで特定可能

```py
raise
```

• 同様に、ここでもエラーを上位に伝える。<br>
• `raise` は “報告のバトン” のようなもので、「`safe_click` 内で失敗したよ」という情報を呼び出し元に渡す<br>
• これで `try～finally` などで上位処理が適切に対処できる。

```py
print("クリック完了")
```

• 通常クリックでも JS クリックでも成功すれば、最終的にこの行に到達<br>
• このログが出ていれば、「少なくともクリック処理としては成功している」ことが確認できる<br>

# `if __name__ == "__main___"`ブロック

```py
if __name__ == "__main__":
    chrome: WebDriver = webdriver.Chrome()
    try:
        chrome.get("https://libecity.com/signin")

        ge = GetElement()
        action = ActionElement()

        id_input = ge.get_by_css(chrome, "input[type='text']")
        action.clear_and_send_keys(id_input, "test@example.com")

        password_input = ge.get_by_css(chrome, "input[type='password']")
        action.clear_and_send_keys(password_input, "test1234")

        login_btn = ge.get_by_css(chrome, "button[type='submit']")
        action.safe_click(login_btn, chrome)

        password_input.send_keys(Keys.ENTER)

        time.sleep(3)
        print(chrome.current_url)
    finally:
        chrome.quit()
```

```py
if __name__ == "__main__":
```

• このファイルが“直接”selenium_manager.py で実行された時だけ、以下の処理を動かす合図<br>
• 逆に、他のファイルから import された場合は、このブロックの中身は実行されない（定義だけ読み込む）<br>
• これにより「ライブラリとして再利用」「スクリプトとして実行」の両立ができる。<br>
• テストコードやデモ実行を同じファイルに置いても安全になる、お約束のガード<br>
• つまりここは「エントリーポイント（スタート地点）宣言」

```py
chrome: WebDriver = webdriver.Chrome()
```

• Chrome ブラウザを新規起動し、その操作ハンドル（リモコン）を chrome 変数に入れている<br>
•`: WebDriver` は型ヒントで、「chrome は WebDriver 型だよ」と人間＆エディタに教えるメモ（動作には影響しない）<br>
• 失敗するときは、Chrome と ChromeDriver のバージョン不一致や権限エラーが多い<br>
• 後でオプションを付けたい時は `webdriver.Chrome(options=opts)` に拡張できる<br>
• 以降、ページ遷移・要素検索・JS 実行など、すべて chrome 経由で命令できる<br>

```py
try:
```

• これ以降の処理を安全に実行するための囲い<br>
• 中でエラーが起きても、後ろの `finally: `が必ず実行されて後片付け（`quit()`）できる<BR>
• Web 自動化はサイト都合で失敗しやすいので、後処理保証は超重要<br>
• どの行で落ちたかの切り分けも、この構造があると行いやすくなる<BR>
• つまり「試す（try）→ 失敗でも掃除」の骨格を作っている

```py
chrome.get("https://libecity.com/signin")
```

• 指定 URL にページ遷移（人間で言うとアドレスバーに URL を入れて Enter）<BR>
• 遷移直後は DOM 構築がまだのことがあるので、要素取得は“すぐ”だと失敗する場面もある<BR>
• 簡易には `time.sleep`、実務では `WebDriverWait` で条件待機にするのが安定<BR>
• ここが通れば、このページの DOM がターゲットになる<BR>
• ネットワーク遮断・証明書・リダイレクトなどで到達に失敗することもある

```py
ge = GetElement()
```

• 取得専用クラスのインスタンスを作成。役割は「要素を見つけること」に限定<BR>
• 取得処理（By/値、ログ、例外）を一ヶ所に集約でき、再利用性・保守性が上がる<BR>
• chrome は都度引数で渡す設計なので、クラス自体は状態を持たない（テストしやすい）<BR>
• 取得のログ書式やリトライ戦略を、ここに追加しても他のコードに影響しない<BR>
• 「探す（Get）」と「操作する（Action）」を分離している点が設計の肝<BR>

```py
action = ActionElement()
```

• 操作専用クラスのインスタンス。責務は「入力・クリック・フォールバック」等の振る舞いに限定<BR>
• ログの出し方や例外の上げ方を統一でき、読みやすく差し替えやすい構造になる<BR>
• 学習段階では `print`、将来は `logger.debug/error` に差し替え可能（設計が対応済み）<BR>
• Get と Action の分離で、変更の波及を最小化している<BR>

```py
id_input = ge.get_by_css(chrome, "input[type='text']")
```

・Chrome 上の Web ページから `<input type='text'>` という入力欄を CSS で探して、その要素を `id_input` という箱に入れておく
という 1 行<BR>
• CSS セレクタでメールアドレス欄の `<input>` を取得（このサイトは type='text'）<BR>
• ここで `NoSuchElementException` が出るなら、描画待ち不足かセレクタ不一致が主原因<BR>
• SPA サイトでは要素の出現が遅いことがあるため、将来的に明示的待機付きの get を生やす余地があり<BR>
• 取得成功すると `id_input` は Selenium の WebElement（操作対象）になる<BR>

```py
action.clear_and_send_keys(id_input, "test@example.com")
```

• 入力欄を一度クリアしてから指定文字列を送信（追記を防ぐ安全パターン）<BR>
• 前後で print ログ（「入力クリア＆開始」「入力完了: …」）が出るので、時系列が追いやすい<BR>
• 失敗時は例外を即`raise`するので、呼び出し側で「どこで落ちたか」が分かります。<BR>
• 実務では IME やマスクがあるケースもある、まずは基本挙動として OK。<BR>
• ここで正しい入力が入り、以降のバリデーションに進める土台ができる。

```py
password_input = ge.get_by_css(chrome, "input[type='password']")
```

• CSS セレクタでパスワード欄の `<input>` を取得（`type='password'`）<BR>
• メール欄とセレクタが違うので、取り間違いを起こしにくくなっている<BR>
• 取得ログが残るため、万一の失敗でも By/値からすぐ特定できる<BR>

```py
action.clear_and_send_keys(password_input, "test1234")
```

• パスワード欄もクリア → 入力でセット（再実行でも同じ値に確定）<BR>
• ここも前後ログにより、入力の有無が目で追える<BR>
• キー送信がブロックされている特殊 UI なら、別の打鍵戦略に切替えが必要になるが、基本は OK。<BR>

```py
login_btn = ge.get_by_css(chrome, "button[type='submit']")
```

• 送信ボタン（ログインボタン）を CSS で取得<BR>
• ここが取れれば、ページ上にボタンが存在していることは確定<BR>
• ただし「存在」と「押せる」は別問題（無効/覆い/画面外など）<BR>
• 取得専用クラスにより、選択子の変更も一箇所で済む<BR>
• 後続で「安全クリック」に渡す<BR>

```py
action.safe_click(login_btn, chrome)
```

• まずは通常の `.click()` を試し、
クリック不可系（`ElementClickInterceptedException` / `ElementNotInteractableException`）なら
JS クリック`（execute_script("arguments[0].click();", element)`へ自動フォールバック<BR>
• これにより、一時的な被り・非表示・アニメ中でも押せる可能性が上がる<BR>
• ただし「押した＝送信」とは限らない（サイトが Enter 送信前提のこともある）<BR>
• ログに「通常クリック不可（エラー種別…）→ JS でフォールバック」が出たら、安全装置が働いた証拠<BR>
• クリック後の反応（遷移 or エラー表示）は、この直後の行で確認する

```py
password_input.send_keys(Keys.ENTER)
```

• キーボードの Enter を送信。多くのフォームで送信（submit）トリガになる<BR>
• これは「入力確定（blur）＋送信」をまとめて起こす効果があり、ボタンに依存しない送信が可能<BR>
• クリックだけでは送信されないサイト（SPA やバリデーション強め）で決め手になる<BR>
• **_いまのコードだと「ボタンクリック → Enter 送信」の二段構えになっており、どちらかが決まれば OK という戦略_**<BR>
• 実務ではどちらか一方に絞る方がログが読みやすいが、学習中はこの保険構成でも問題ない

```py
time.sleep(3)
```

• 以降の確認（URL 出力）前に固定 3 秒の待機を入れ、遷移や描画を待っている<BR>
• 速い環境では無駄、遅い環境では不足、という弱点あり<BR>
• 実務では `WebDriverWait` に置き換え、条件成立まで待機するのが理想<BR>
• ただし学習段階では挙動の見通しが良く、簡潔という利点がある<BR>
• このあと `current_url` を見るので、その前の小休止という位置づけ

```py
print(chrome.current_url)
```

• 現在の URL を出力し、ログイン後に URL が変化したかを目で確認できる<BR>
• 期待通りなら /mypage/home などに変わり、成功の証跡になる<BR>
• 変わらなければ、フォームがサーバ側で弾かれて同一ページにいる可能性（ページ内エラー表示型）がある<BR>
• ここまでのログ（クリック →Enter→URL）を見れば、詰まりポイントの切り分けが可能

```py
finally:
```

• `try` 内でエラーが起きても起きなくても、必ずこのブロックが実行される<br>
• ここで終了処理（ブラウザ終了）を行い、リソースリークを防ぐ<BR>
• 異常終了時でも“ブラウザが残り続ける”問題を避けられる<BR>
• 自動タスクを何度も回すときは特に重要となる<BR>
• 「後始末の保証」を与える枠、という理解で OK

```py
chrome.quit()
```

• ブラウザプロセス全体を終了する。`close()` がタブ閉じなのに対し、`quit()` はセッション終了<BR>
例外で落ちた場合でも必ず呼ばれる（finally:の恩恵）<BR>
• デバッグ時はここで止めておくと、画面を目視確認できる（ブレークポイント活用）<BR>
• これで一連の自動操作はクリーンに完了となる

---

### 補足：今の並び（クリック →Enter）について<BR>• 現状：safe_click のあとに ENTER を送っている（“二段構え”）<BR>• 効果：どちらかが効けば送信成功。学習中は OK。

    •	実務の整理案：
    •	クリックが素直に効くサイト → safe_click だけ
    •	Enter送信が正解のサイト → Keys.ENTER だけ
    •	どちらかに絞るとログが読みやすく、原因切り分けもしやすくなる。

<BR><BR><BR>

# ActionElement

# GEMINI が出したコード

#### 💻 統合された実装コード (selenium_manager.py)

あなたの学習段階では logger を使わず print で代用する、という指示に基づき、logger クラスの代わりとなる簡単な Logger クラスを定義し、そのメソッド内で print を使う形で実装します。

#### 📄 selenium_manager.py (動作確認用 Logger 代用版)

```py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.chrome.options import Option
import sys
import time

# # ----------------------------------------------------

# # ⚠️ 注意: 本来は logging モジュールを使うが、今回は print で代用

# # ----------------------------------------------------

class SimpleLogger:

"""logger の代わりとして print を行うクラス"""

def debug(self, msg):
print(f"[DEBUG] {msg}")
def error(self, msg):
print(f"[ERROR] {msg}", file=sys.stderr)

# ----------------------------------------------------
class ActionElement:

"""Selenium の要素操作専用クラス"""

def **init**(self, logger):

"""

初期化メソッド

引数: logger（logging.Logger）

"""

self.logger = logger

# Chrome は保持しない。(GetElement 側で使用するため)

# self.logger.debug("ActionElement クラス 初期化完了") # 通常はここにログを入れる

# --- メソッド（必ずこの順序で定義）---

def send_keys(self, element: WebElement, text: str) -> None:

"""指定の要素にテキストを入力する"""

try:
self.logger.debug("入力開始")
element.send_keys(text)
self.logger.debug(f"入力完了: {text}")
except Exception as e:
self.logger.error(f"操作失敗: {e}")
raise

def click(self, element: WebElement) -> None:
"""指定の要素をクリックする"""
try:
self.logger.debug("クリック開始")
element.click()
self.logger.debug("クリック完了")
except Exception as e:
self.logger.error(f"操作失敗: {e}")
raise

def clear_and_send_keys(self, element: WebElement, text: str) -> None:
"""要素をクリアしてからテキストを入力する"""
try:
self.logger.debug("入力クリア＆開始")
element.clear()
element.send_keys(text)
self.logger.debug(f"入力完了: {text}")
except Exception as e:
self.logger.error(f"操作失敗: {e}")
raise

def safe_click(self, element: WebElement, chrome: WebDriver) -> None:
"""通常クリックを試行し、失敗した場合に JavaScript でクリックする

:param element: 対象の WebElement

:param chrome: WebDriver インスタンス（JavaScript 実行用）

"""

self.logger.debug("クリック開始")
try:
element.click()
except (ElementClickInterceptedException, ElementNotInteractableException) as e:

# クリックが邪魔された場合や操作不能な場合、JavaScript でフォールバック

self.logger.debug(f"クリック失敗（エラー: {type(e).**name**}）。JavaScript で再試行。")
try:

# JavaScript でクリックする

chrome.execute_script("arguments[0].click();", element)
except Exception as js_e:
self.logger.error(f"JavaScript クリック失敗: {js_e}")
raise

except Exception as e:
# その他の予期せぬエラー
self.logger.error(f"操作失敗: {e}")
raise

self.logger.debug("クリック完了")

# ----------------------------------------------------

# テスト実施要件（if **name** == "**main**": ブロック）

# ----------------------------------------------------

if **name** == "**main**":

# 実際には GetElement クラスも必要だが、ここでは要素を直接取得する処理で代用

# 1. WebDriver の起動

options = Options()

# options.add_argument('--headless') # ヘッドレスモード（画面非表示）で実行したい場合はコメントアウトを外す

try:
driver = webdriver.Chrome(options=options) # WebDriver（ブラウザ）を起動

except Exception as e:
print(f"WebDriver の起動に失敗しました。Chrome ドライバーのパスやバージョンを確認してください: {e}", file=sys.stderr)
sys.exit(1)

# 簡易ロガー（print 代用）をインスタンス化

my_logger = SimpleLogger()

# 2. ActionElement クラスをインスタンス化（ここで**init**が呼ばれる）

action_element = ActionElement(logger=my_logger) # action_element 変数にクラスの実体（インスタンス）を代入

# 3. 対象 URL へアクセス

target_url = "https://libecity.com/signin"
driver.get(target_url)
time.sleep(2) # 読み込み待ち

try:
# 要素の特定（ここでは ID で直接取得）
# 「リベのログインサイトの ID 入力欄」
id_input_locator = "id_username" # サイトの要素によって変更の可能性あり
username_element = driver.find_element("id", id_input_locator)

# 「リベのログインサイトのログインボタン」
login_button_locator = "js-signin-button" # サイトの要素によって変更の可能性あり

login_button_element = driver.find_element("id", login_button_locator)

test_text = "test_user_001"

my_logger.debug("--- send_keys のテスト開始 ---")

# 4. ActionElement のメソッドで「ID 入力欄」に文字列を入力
action_element.send_keys(element=username_element, text=test_text)
my_logger.debug("--- send_keys のテスト完了 ---")
time.sleep(1)
my_logger.debug("--- clear_and_send_keys のテスト開始 ---")

# 5. ActionElement のメソッドで「ID 入力欄」をクリアして再入力
action_element.clear_and_send_keys(element=username_element, text="retest_002")

my_logger.debug("--- clear_and_send_keys のテスト完了 ---")
time.sleep(1)
my_logger.debug("--- click のテスト開始 ---")

# 6. ActionElement のメソッドで「ログインボタン」をクリック

# ※ 実際には ID やパスワードがないためエラー画面に遷移します
action_element.click(element=login_button_element)
my_logger.debug("--- click のテスト完了 ---")

# safe_click のテストはフォールバックエラーを起こす環境構築が複雑なため割愛

except Exception as e:

my_logger.error(f"テスト中にエラーが発生しました: {e}")

finally:

# テスト終了

time.sleep(3)
driver.quit() # ブラウザを閉じる
```

# 🛠️ 修正版コード：**init**不使用と print 代用

**init**を使わない場合、logger（またはその代わりの SimpleLogger）は各メソッドを呼び出すたびに引数として渡す必要があります。

# 📄 selenium_manager.py (修正版)

```py
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.remote.webelement import WebElement

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import sys

import time

# ----------------------------------------------------

# 💡 変更点 1: logger の代わりとして print を行うクラス (SimpleLogger)

# ----------------------------------------------------

class SimpleLogger:

"""logger の代わりとして print を行うクラス"""

def debug(self, msg):

print(f"[DEBUG] {msg}")

def error(self, msg):

print(f"[ERROR] {msg}", file=sys.stderr)

# ----------------------------------------------------

class ActionElement:

"""Selenium の要素操作専用クラス (init 不使用版)"""

# 💡 変更点 2: **init** メソッドを削除

# 初期化が不要になったため、このクラスは「単なる機能のまとまり」として使われる

pass

# --- メソッド（必ずこの順序で定義）---

# 💡 変更点 3: 全メソッドの引数に logger (SimpleLogger) を追加

def send_keys(self, element: WebElement, text: str, logger: SimpleLogger) -> None:

"""指定の要素にテキストを入力する"""

try:

logger.debug("入力開始")

element.send_keys(text)

logger.debug(f"入力完了: {text}")

except Exception as e:

logger.error(f"操作失敗: {e}")

raise

def click(self, element: WebElement, logger: SimpleLogger) -> None:

"""指定の要素をクリックする"""

try:

logger.debug("クリック開始")

element.click()

logger.debug("クリック完了")

except Exception as e:

logger.error(f"操作失敗: {e}")

raise

def clear_and_send_keys(self, element: WebElement, text: str, logger: SimpleLogger) -> None:

"""要素をクリアしてからテキストを入力する"""

try:

logger.debug("入力クリア＆開始")

element.clear()

element.send_keys(text)

logger.debug(f"入力完了: {text}")

except Exception as e:

logger.error(f"操作失敗: {e}")

raise

def safe_click(self, element: WebElement, chrome: WebDriver, logger: SimpleLogger) -> None:

"""

通常クリックを試行し、失敗した場合に JavaScript でクリックする

:param element: 対象の WebElement

:param chrome: WebDriver インスタンス（JavaScript 実行用）

:param logger: SimpleLogger インスタンス

"""

logger.debug("クリック開始")

try:

element.click()

except (ElementClickInterceptedException, ElementNotInteractableException) as e:

# クリックが邪魔された場合や操作不能な場合、JavaScript でフォールバック

logger.debug(f"クリック失敗（エラー: {type(e).**name**}）。JavaScript で再試行。")

try:

# JavaScript でクリックする

chrome.execute_script("arguments[0].click();", element)

except Exception as js_e:

logger.error(f"JavaScript クリック失敗: {js_e}")

raise

except Exception as e:

# その他の予期せぬエラー

logger.error(f"操作失敗: {e}")

raise

logger.debug("クリック完了")

# ----------------------------------------------------

# テスト実施要件（if **name** == "**main**": ブロック）

# ----------------------------------------------------

if **name** == "**main**":

options = Options()

try:

driver = webdriver.Chrome(options=options)

except Exception as e:

print(f"WebDriver の起動に失敗しました。Chrome ドライバーのパスやバージョンを確認してください: {e}", file=sys.stderr)

sys.exit(1)

# 簡易ロガー（print 代用）をインスタンス化

my_logger = SimpleLogger()

# 💡 変更点 4: ActionElement のインスタンス化

# **init**がないため、引数は不要。ただし、クラスの実体（インスタンス）は作る必要がある。

action_element = ActionElement()

target_url = "https://libecity.com/signin"

driver.get(target_url)

time.sleep(2)

try:

id_input_locator = "id_username" # ID 入力欄のロケーター

username_element = driver.find_element("id", id_input_locator)

login_button_locator = "js-signin-button" # ログインボタンのロケーター

login_button_element = driver.find_element("id", login_button_locator)

test_text = "test_user_001"

my_logger.debug("--- send_keys のテスト開始 ---")

# 💡 変更点 5: メソッド呼び出し時に my_logger を引数として渡す

action_element.send_keys(element=username_element, text=test_text, logger=my_logger)

my_logger.debug("--- send_keys のテスト完了 ---")

time.sleep(1)

my_logger.debug("--- clear_and_send_keys のテスト開始 ---")

# 💡 変更点 5: メソッド呼び出し時に my_logger を引数として渡す

action_element.clear_and_send_keys(element=username_element, text="retest_002", logger=my_logger)

my_logger.debug("--- clear_and_send_keys のテスト完了 ---")

time.sleep(1)

my_logger.debug("--- click のテスト開始 ---")

# 💡 変更点 5: メソッド呼び出し時に my_logger を引数として渡す

action_element.click(element=login_button_element, logger=my_logger)

my_logger.debug("--- click のテスト完了 ---")

# safe_click のテストの呼び出し例（logger と driver も渡す）

# action_element.safe_click(element=login_button_element, chrome=driver, logger=my_logger)

except Exception as e:

my_logger.error(f"テスト中にエラーが発生しました: {e}")

finally:

time.sleep(3)

driver.quit()
```

# ChatGPT が出したコード

```py
from **future** import annotations

import time

from typing import Iterable, Tuple

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (

TimeoutException,

WebDriverException,

ElementClickInterceptedException,

ElementNotInteractableException,

)

class ActionElement:

"""要素に対する操作だけを担当するクラス（print でログ出力する簡易版）。"""

def **init**(self) -> None:

"""この学習版では logger を使わないので、特に保持する状態はありません。"""

pass

def send_keys(self, element: WebElement, text: str) -> None:

"""指定要素に文字列を入力する。操作前後でログを出す。"""

try:

print("入力開始")

element.send_keys(text)

print(f"入力完了: {text}")

except Exception as e: # 予期しない例外も含めて必ず伝播

print(f"操作失敗: {e}")

raise

def click(self, element: WebElement) -> None:

"""指定要素をクリックする。操作前後でログを出す。"""

try:

print("クリック開始")

element.click()

print("クリック完了")

except Exception as e:

print(f"操作失敗: {e}")

raise

def clear_and_send_keys(self, element: WebElement, text: str) -> None:

"""一度クリアしてから入力する。操作前後でログを出す。"""

try:

print("入力クリア＆開始")

element.clear()

element.send_keys(text)

print(f"入力完了: {text}")

except Exception as e:

print(f"操作失敗: {e}")

raise

def safe_click(self, element: WebElement, chrome: WebDriver) -> None:

"""通常クリックが妨げられたら JS クリックでフォールバックする安全版。"""

try:

print("クリック開始")

try:

element.click()

except (ElementClickInterceptedException, ElementNotInteractableException):

print("通常クリック不可 → JavaScript クリックでフォールバック")

chrome.execute_script("arguments[0].click();", element)

print("クリック完了")

except Exception as e:

print(f"操作失敗: {e}")

raise

# --- 補助関数（学習用）: 候補ロケータを順に試して最初に見つかった要素を返す ---

def find_first(chrome: WebDriver, candidates: Iterable[Tuple[str, str]], timeout: int = 10) -> WebElement:

last_error: Exception | None = None

for by, value in candidates:

try:

return WebDriverWait(chrome, timeout).until(

EC.presence_of_element_located((by, value))

)

except Exception as e:

last_error = e

# どれも見つからなかった場合は最後のエラーを再送出

if last_error:

raise last_error

raise TimeoutException("No candidates matched.")

# --- ロケータ候補（対象ページの DOM 変化に多少強いように複数用意） ---

ID_INPUT_CANDIDATES = [

(By.ID, "email"),

(By.NAME, "email"),

(By.CSS_SELECTOR, "input[type='email']"),

(By.ID, "username"),

(By.NAME, "username"),

(By.CSS_SELECTOR, "input[autocomplete='username']"),

(By.CSS_SELECTOR, "input[type='text']"),

]

LOGIN_BUTTON_CANDIDATES = [

(By.CSS_SELECTOR, "button[type='submit']"),

(By.XPATH, "//button[contains(., 'ログイン')]")

,

(By.XPATH, "//button[contains(., 'Login') or contains(., 'Sign in') or contains(., 'サインイン')]")

,

(By.CSS_SELECTOR, "input[type='submit']"),

]

# --- GetElement が未実装でもテストできるように学習用の簡易版を同名で用意 ---

try:

GetElement # 既にどこかで定義済みならそれを使う

except NameError: # なければ簡易版を定義

class GetElement:

def **init**(self, chrome: WebDriver) -> None:

self.chrome = chrome

def first(self, candidates: Iterable[Tuple[str, str]], timeout: int = 10) -> WebElement:

return find_first(self.chrome, candidates, timeout)

# --- 簡易テスト（課題指示どおり末尾に設置） ---

if **name** == "**main**":

# 1) Chrome 起動

chrome: WebDriver = webdriver.Chrome()

try:

# 2) 対象ページへ

chrome.get("https://libecity.com/signin")

# 3) GetElement を用意

ge = GetElement(chrome)

# 4) ID 入力欄の取得（候補を順に試す）

id_input: WebElement = ge.first(ID_INPUT_CANDIDATES, timeout=15)

# 5) 操作用クラスの用意（print 版）

action = ActionElement()

# 6) クリアしてから任意の文字列を入力

action.clear_and_send_keys(id_input, "test@example.com")

# 7) ログインボタンを取得

login_btn: WebElement = ge.first(LOGIN_BUTTON_CANDIDATES, timeout=15)

# 8) 安全クリック（通常 →JS フォールバック）

action.safe_click(login_btn, chrome)

# 9) 観察用に少し待つ（学習用途）

time.sleep(2)

finally:

# 10) 終了

chrome.quit()
```
