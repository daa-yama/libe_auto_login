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
            raise e -->
```
