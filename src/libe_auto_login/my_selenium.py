# 進め方　
# AIにコードを作成してもらう→動作を確認、修正→作ったコードをAIに一行づつ解説してもらう（chatGPTとGEMINIなど双方向から解説してもらうと理解が深まる）

# --- 必要最小限のインポート ---
from selenium import webdriver
# selenium本体のリモコンであるwebdriverを取り込み道具として使う（webdriverはwebブラウザを動かすための運転手の役目）

from selenium.common.exceptions import TimeoutException, WebDriverException
# エラー処理のために、TimeoutException（待っても要素が出ない）とWebDriverException（ブラウザがうまく起動しない）を取り込む
# 	これらを try/except で捕まえることで、原因ごとの対処やわかりやすいログが書ける。

from selenium.webdriver.chrome.options import Options
# Chromeの起動設定を作るためのクラス Options を読み込み

from selenium.webdriver.common.by import By
# ウェブページ上の要素をどうやって探すかという「探し方リスト」
# 例えば、「IDで探す」「名前で探す」「XPATHという特別な方法で探す」といった様々なルールが詰まっている。
# このリストを使うことで、目的の要素を正確に見つけ出すことができる。	
# 例）By.ID, By.NAME, By.CSS_SELECTOR, By.XPATH など。
# 要素の探索方法を指定するためのByを取り込む

from selenium.webdriver.support import expected_conditions as EC
# 要素が「どうなったらOKか」という「条件チェックリスト」。例えば、「要素がクリックできる状態になったらOK」といった条件を判断するのに使いる。	
# 「〜になるまで待つ」条件セットを EC という短い名前で使えるようにする。　expected_conditions as EC
# 例えば、「要素がクリック可能になるまで待つ」「要素が表示されるまで待つ」などの条件が含まれている。
# これを使うことで、ページの読み込みや動的な変化に対応しやすくなる。        

from selenium.webdriver.support.ui import WebDriverWait
# 「〜になるまで待つ」ための道具 WebDriverWait を取り込む
# 条件が整うまで最大N秒だけ待つタイマーを使えるようにする。
# プログラムはウェブサイトの読み込みよりずっと速く動くので、この道具を使ってページが完全に読み込まれるまで待つ必要がある。
# これを使うことで、ページの読み込みや動的な変化に対応しやすくなる。

# この7行で、
# **起動（webdriver / Options）・探索（By）・待機（WebDriverWait + EC）・エラー処理（Exceptions）**
# の全部が使えるようになる。

# ========== 1) ChromeDriverManager ==========
class ChromeDriverManager:
    # ChromeDriverManager という道具の設計図を作る
    # ChromeDriverManager は ChromeDriver を起動するための道具
    # ※ 型ヒントやデコレーターは使っていない。Pythonの基本機能だけで書いている。
    
    def __init__(self, window_width=1280, window_height=800):
        #   「__init__（イニシャライズ）」という名前の初期化メソッド
        #   ChromeDriverManager() で道具を作るときに、ウィンドウサイズを指定できるようにする
        #   指定しなければ、1280x800 になる （横x縦）       
        
        self.window_width = window_width
        # 受け取った値を自分の持ち物（インスタンス変数）として保存。    
        # ウィンドウ幅を保存      
        
        self.window_height = window_height
        # ウィンドウ高さを保存  
        

    def chrome_option(self):
        # Chromeの起動オプションを設定するメソッド
        # 例えば、ウィンドウサイズやページ読み込みの待ち方などを指定する    
        
        options = Options()
        # Options クラスのインスタンスを作る。これが Chrome の起動設定を作るための道具になる。      
        # ページの読み込み完了待ちを軽めに（DOM（ドキュメントオブジェクトモデル）構築で先へ進む）
        
        options.page_load_strategy = "eager"
        # Chromeの起動オプションに、ページの読み込み完了待ちを「eager（軽め）」に設定する。
        # これにより、ページのDOMが構築された時点で次の操作に進むようにな理、ページの読み込みが完全に終わるのを待たずに、より速く操作を開始できる。
        # ただし、ページ内のすべてのリソース（画像や広告など）が読み込まれる前に操作が始まる可能性がある。
        # そのため、ページの動作に影響が出る場合は "normal" に戻すことも検討する。
        
        options.add_argument(f"--window-size={self.window_width},{self.window_height}")
        # Chromeの起動オプションに、ウィンドウサイズを指定する引数を追加する。
        # 例えば、"--window-size=1280,800" のような形になる
        # 指定されたサイズで開くので、画面のレイアウトが変わるウェブサイトでも、安定して操作できるようになる。        
        
        print(f"[INFO] Chrome のオプションを設定しました: {self.window_width}x{self.window_height}")
        # 設定したオプションをログに出力する    
        
        return options
        # 作ったオプションを呼び出し元に返す  

    def chrome_process(self):
        # ChromeDriver を立ち上げるメソッド   driverを受け取るだけ。
        
        try:
        #エラーが起きるかもしれない処理を囲むためのもの。
        # もしこの中のコードでエラーが起きても、プログラムが途中で止まらず、次のexceptの処理に飛ぶことができる。
        
            options = self.chrome_option()
            # 先ほど作った chrome_option メソッドを呼び出して、Chromeの起動オプションを取得する。   
            
            driver = webdriver.Chrome(options=options) 
            # ChromeDriver を起動する。引数に先ほど作ったオプションを渡す。
            # これで、指定したオプション（ウィンドウサイズやページ読み込み待ちなど）を使ってChromeが起動する。
            # Selenium Manager が自動解決
            # 暗黙待機は使わない（速さと安定のため）
            
            print("[INFO] Chrome driver が正常に起動しました。")
            # 起動成功のログを出力する 
            
            return driver
            # 起動した driver を呼び出し元に返す
        
        except WebDriverException as e:
            # WebDriverException（ブラウザがうまく起動しない）を捕まえる
            
            print(f"[ERROR] Chrome 起動に失敗しました: {e}")
            # エラーメッセージをログに出力する
            
            raise
            # エラーを呼び出し元に伝える（ここで止めずに、呼び出し元でさらに処理できるようにするため）
            
        except Exception as e:
            # その他の予期せぬエラーを捕まえる
            print(f"[ERROR] Chrome 起動中に予期せぬエラー: {e}")
            raise
            


# ========== 2) GetElement ==========

class GetElement:
    # GetElement は ウェブページ上の要素（ボタンや入力欄など）を正確に探し出すための道具
        
    def __init__(self, driver, wait_seconds=8):
        # GetElement(driver, wait_seconds=8) で道具を作るときに、driver と待ち時間を指定できるようにする
        # driver は ChromeDriver のインスタンス
        # wait_seconds は要素が見つかるまでの最大待ち時間（秒）。指定しなければ 8 秒になる  
        
        self.driver = driver
        #   受け取った driver を自分の持ち物（インスタンス変数）として保存。
        
        self.wait = WebDriverWait(driver, wait_seconds)
        # WebDriverWait クラスのインスタンスを作る。これがタイマーの要素。「〜になるまで待つ」ための道具になる。
        # 引数に driver と 待ち時間（秒）を渡す。
        # これを使って、要素が見つかるまで最大 wait_seconds 秒だけ待つことができる。
        

    def _wait_for(self, by, value, clickable=False, visible=False):
        # 内部メソッド _wait_for を定義。要素を探して、見つかるまで待つ。
        # 引数 by と value で要素の探し方と値を指定する。
        # by と value は「探し方（By.X）と住所（文字列）」のセット
        # clickable=True なら、要素がクリックできる状態になるまで待つ
        # visible=True なら、要素が表示されるまで待つ
        # どちらも False 。何も指定しなければ「存在するだけ」で良しとする
        
        try:
            locator = (by, value)
            #   locator という変数に、(by, value) のタプルを作る。これが要素の住所になる。
            
            if clickable:
                # clickable=True なら、要素がクリックできる状態になるまで待つ
                
                elem = self.wait.until(EC.element_to_be_clickable(locator))
                # self.wait.until(...) で、要素がクリックできる状態になるまで待つ。
                # EC.element_to_be_clickable(locator) は、要素がクリックできる状態になる条件を表す。
                # 要素がクリックできる状態になったら、その要素を elem に保存する。
                
            elif visible:
                #visible=True なら、要素が表示されるまで待つ
                
                elem = self.wait.until(EC.visibility_of_element_located(locator))
                # self.wait.until(...) で、要素が表示されるまで待つ。
                # EC.visibility_of_element_located(locator) は、要素が表示される条件を表す。
                # 要素が表示されたら、その要素を elem に保存する。  
            else:
                
                elem = self.wait.until(EC.presence_of_element_located(locator))
                # self.wait.until(...) で、要素が存在するまで待つ。
                # EC.presence_of_element_located(locator) は、要素が存在する条件を表す。
                # 要素が存在したら、その要素を elem に保存する。
                
            print(f"[INFO] 要素を取得しました: by={by}, value={value}")
            #  要素を取得したログを出力する    
            
            return elem
            # 取得した要素を呼び出し元に返す
            
        except TimeoutException:
            # TimeoutException（待っても要素が出ない）を捕まえる
            # 待機が上限時間を超えたときにここに来る
            # 「見つからなかった」ことを正しく扱うための分岐
            
            path = "debug_not_found.png"
            #スクリーンショットの保存先パスを指定
            
            try:
                # スクリーンショットを撮る
                
                self.driver.save_screenshot(path)
                # driver.save_screenshot(path) で、現在の画面のスクリーンショットを撮って、指定したパスに保存する。
                
            except Exception:
                #  スクリーンショット撮影に失敗しても無視する
                pass
            print(f"[ERROR] 要素が見つかりません: by={by}, value={value}")
            # エラーメッセージをログに出力する
            
            print(f"[DEBUG] url={self.driver.current_url}, title={self.driver.title}, screenshot={path}")
            # デバッグ情報をログに出力する（現在のURL、タイトル、スクリーンショットのパス）
            raise
        # エラーを呼び出し元に伝える（ここで止めずに、呼び出し元でさらに処理できるようにするため）

    def open_email_login_tab(self):
        # 「メールアドレスでログイン」タブを開くメソッド
        # もしタブが見つからなければスキップする
        try:
            tab = self._wait_for(
                By.XPATH,
                "//*[contains(., 'メールアドレスでログイン')][self::button or self::a or self::div]",
                clickable=True,
                visible=True,
            )
            #   _wait_for メソッドを使って、「メールアドレスでログイン」タブの要素を探す。
            # XPATH で「メールアドレスでログイン」という文字を含むボタン/リンク/div要素を探す。
            # visible=True で見えるまで、clickable=True で押せるまで待つ
            # 見つかった要素を tab に保存する。 
            
            tab.click()
            # 見つかったタブ要素をクリックして開く
            
            print("[INFO] 『メールアドレスでログイン』タブをクリックしました。")
            # クリックしたログを出力する
        
        except TimeoutException:
            print("[INFO] タブが見つからないのでスキップします。")
            # タブが見つからなければスキップする

    def get_id_element(self):
        # メール欄：ORで一発
        return self._wait_for(
            By.XPATH,
            "//input[@type='email' or @name='email' "
            " or contains(@id,'mail') or contains(@name,'mail') "
            " or contains(@placeholder,'メール') or contains(@aria-label,'メール')]",
            visible=True,
        )
        # メールアドレス入力欄の要素を探す
        # XPATH で input 要素を探す。
        # type='email' または name='email' または id/name に 'mail' を含む、
        # または placeholder/aria-label に 'メール' を含むものを対象とする
        # visible=True で要素が表示されるまで待つ
        # 見つかった要素を返す
        

    def get_pass_element(self):
        # パスワード欄：ORで一発
        return self._wait_for(
            By.XPATH,
            "//input[@type='password' or @name='password' "
            " or contains(@id,'pass') or contains(@name,'pass') "
            " or contains(@placeholder,'パスワード') or contains(@aria-label,'パスワード')]",
            visible=True,
        )
        # パスワード入力欄の要素を探す
        # XPATH で input 要素を探す。
        # type='password' または name='password' または id/name に 'pass' を含む、
        # または placeholder/aria-label に 'パスワード' を含むものを対象とする
        # visible=True で要素が表示されるまで待つ
        # 見つかった要素を返す

    def get_check_box_element(self):
        # あれば取得。無ければ呼び出し側で例外を拾ってスキップ
        return self._wait_for(
            By.XPATH,
            "//input[@type='checkbox' or @name='remember' "
            " or //label[contains(., 'ログインしたまま')]/preceding::input[@type='checkbox'][1]]",
            clickable=True,
            visible=True,
        )
        # チェックボックスの要素を探す
        # XPATH で input 要素を探す。
        # type='checkbox' または name='remember' または
        # 「ログインしたまま」という文字を含むラベルの直前にあるチェックボックスを対象とする
        # clickable=True で要素がクリックできる状態になるまで待つ
        # visible=True で要素が表示されるまで待つ
        # 見つかった要素を返す              

    def get_login_btn_element(self):
        # 送信ボタン：ORで一発
        return self._wait_for(
            By.XPATH,
            "//*[self::button or self::input][@type='submit' or contains(normalize-space(.),'ログイン')]",
            clickable=True,
            visible=True,
        )
        #ログインボタンの要素を探す
        # XPATH で button または input 要素を探す。
        # type='submit' または ボタンのテキストに 'ログイン' を含むものを対象とする
        # clickable=True で要素がクリックできる状態になるまで待つ
        # visible=True で要素が表示されるまで待つ
        # 見つかった要素を返す


# ========== 3) ActionElement ==========
class ActionElement:
    # ActionElement は ウェブページ上の要素（ボタンや入力欄など）に対して行動(Action)の操作を行うための道具。動かす係
    
    def __init__(self, driver):
        self.driver = driver
        # 受け取った driver を自分の持ち物（インスタンス変数）として保存。
        # driver は ChromeDriver のインスタンス

    def input_element(self, element, text, clear=True):
        # 入力欄 element に text を入力するメソッド
        # clear=True なら、入力前に既存の文字を消す 
        
        try:
            if clear:
                #clear=True なら、入力前に既存の文字を消す
                element.clear()
                # element.clear() で、入力欄の既存の文字を消す
                
            element.send_keys(text)
            # element.send_keys(text) で、指定された text を入力欄に入力する
            
            print(f"[INFO] 入力しました: {text}")
            # 入力したログを出力する
            
        except Exception as e:
            # その他の予期せぬエラーを捕まえる
            
            print(f"[ERROR] 入力に失敗しました: {e}")
            
            # エラーメッセージをログに出力する
            
            raise
            # エラーを呼び出し元に伝える（ここで止めずに、呼び出し元でさらに処理できるようにするため）
            
    def click_element(self, element):
        # ボタン element をクリックするメソッド
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            # 要素が画面内に収まるようにスクロールする
            
            element.click()
            # element.click() で、指定された要素をクリックする
            
            print("[INFO] 要素をクリックしました。")
            # クリックしたログを出力する
            
        except Exception as e:  
            # その他の予期せぬエラーを捕まえる
            print(f"[ERROR] クリックに失敗しました: {e}")
            # エラーメッセージをログに出力する
            raise
            # エラーを呼び出し元に伝える（ここで止めずに、呼び出し元でさらに処理できるようにするため）