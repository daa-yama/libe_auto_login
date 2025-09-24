# 入口→下請け→内部用

from selenium import webdriver
# seleniumはWEBブラウザを自動で動かすアプリ。seleniumという道具箱からwebdriverという運転役の道具を借りてきますよというイメージ

from selenium.webdriver.chrome.service import Service
# .ドットはフォルダ（パッケージ）やファイル（モジュール）の階層の区切り
# selenium → webdriver → chrome → service モジュールの中にある Service クラスを取り出す、という意味。
# from パッケージ.サブパッケージ.モジュール import 名前
# Service＝「ChromeDriverをどう起動・管理するか（実行係）」

from selenium.webdriver.chrome.options import Options
# Options＝「Chromeをどういう設定で起動するか（レシピ）」

class ChromeManager:
# 「ChromeManager」という名前のクラスを定義。「クラス」とは、複数の関連する関数やデータをひとまとめにして扱うための「設計図」のようなもの。



	def open_site(self, url):
    #  open_siteという名前のメソッド（クラスの中に定義された関数)を定義しています。
    # メソッドを定義する時は、必ず最初の引数にself（セルフ）と書く
    # selfは「このクラス自身」を意味し、このクラスが持っている他のメソッドや変数にアクセスするために必要。
    # urlは、WebサイトのURLを受け取るための引数。このメソッドを呼び出すときに、開きたいサイトのURLをここに渡す。

		chrome = self.start_chrome()
#   ここでは、「start_chrome」という別のメソッドを呼び出している。このメソッドは、Chromeブラウザを起動する処理を担当。
# self.start_chrome()は、「このクラス自身が持っているstart_chromeというメソッドを実行」という命令。それをchromeという変数に入れている

		print(f"これからサイトを立ち上げます")
# 進捗を知らせるメッセージ。プログラムが今何をしているのかを明確にし、**デバッグ（プログラムの誤りを見つける作業）**を助ける役割も果たす。

		chrome.get(url)
# chromeは、先ほどself.start_chrome()メソッドで取得した「起動済みのChromeブラウザ」
# .get(url)は、そのChromeブラウザに「指定したurlのサイトにアクセス」と命令
# この命令により普段手動で行っている「アドレスバーにURLを入力してEnterキーを押す」という操作が自動で行われる

		print(f"サイトを立ち上げました{url}")
# 進捗を知らせる。URLを入れることでどのサイトを立ち上げたかわかる
	



	def start_chrome(self):
#このメソッドは、Chromeブラウザを起動し、そのインスタンス（実体）を返すことを目的としている
# ブラウザの起動という独立した処理を別のメソッドに切り出すことで、コードの再利用性が高まる

		service = Service()
# Serviceというクラスのインスタンス（実体）を作成。serviceという変数に代入。このserviceインスタンスは、Chromeを起動する際に必要な設定情報を持つ

		chrome_options = self.get_chrome_options()
# このメソッド内で、「get_chrome_options」という別のメソッドを呼び出しています。
# self.get_chrome_options()は、「このクラス自身が持っているget_chrome_optionsというメソッドを実行」という命令。
# このメソッドが返してきた結果（Chromeの設定情報）を、chrome_optionsという変数に代入。

		print(f"これからブラウザを起動します")

		chrome = webdriver.Chrome(service=service, options=chrome_options)
#  このコード重要！！！！このコードで実際に動作させることができる。
# webdriver.Chrome()は、webdriverライブラリのChromeクラスのインスタンスを作成することで、Chromeブラウザを起動。
# 引数として、先ほど作成したserviceインスタンスとchrome_optionsインスタンスを渡すことで、
# 特定のサービス設定やオプション設定を適用してChromeを起動することができる。
# chromeという変数には、起動したChromeブラウザの実体が格納。

# service=service,chrome=...???と変数名で混乱したら下記のようにもできると覚えておく
# my_service = Service()
# my_options = Options()
# driver = webdriver.Chrome(service=my_service, options=my_options)

		print(f"ブラウザを起動できました")
		return chrome
# return（リターン）は、関数の処理を終えて、呼び出し元に値を返すための命令。
# このメソッドを呼び出した場所（今回はopen_siteメソッド内）に、chrome変数に格納された「起動したChromeブラウザ」を返す。
# これにより、open_siteメソッドのchrome = self.start_chrome()という行で、Chromeブラウザを受け取ることができる。



	def get_chrome_options(self):
# start_chromeメソッドの中で呼び出されていた、get_chrome_optionsというメソッドの定義部分
# このメソッドは、Chromeブラウザを起動する際のオプション設定を返すことを目的としている。

		chrome_options = Options()
# Optionsクラスのインスタンス（実体）を作成し、chrome_optionsという変数に代入

		chrome_options.add_argument("--window-size=840,600")
# 先ほど作成したchrome_optionsという箱に対して、add_argument（引数を追加する）という命令を実行
# Chromeブラウザのウィンドウサイズを「幅840ピクセル、高さ600ピクセル」に設定
# このように、オプション設定を別のメソッドに切り出すことで、
# ウィンドウサイズを変えたい時も、このメソッドの中だけを修正すれば済むようになり、変更が容易になる

		return chrome_options
# このメソッドの処理を終え、設定済みのchrome_optionsインスタンスを呼び出し元に返す

libe_url = "https://site.libecity.com/"
yahoo_url = "https://yahoo.co.jp"
chrome_manager = ChromeManager()
# 定義したクラスを使って、プログラムを実行する部分
# libe_urlとyahoo_urlという変数に、それぞれのURLを代入
# chrome_manager = ChromeManager()は、ChromeManagerというクラスのインスタンス（実体）を作成、chrome_managerという変数に代入しています。
# これにより、先ほど設計図として定義したChromeManagerが、実際に動く「道具」として使えるようになる

# chrome_manager.open_site(url = libe_url)

chrome_manager.open_site(url = yahoo_url)
# この最後の部分が、実際にプログラムを動かす命令
# chrome_manager.open_site()は、「chrome_managerという道具（インスタンス）のopen_siteというメソッドを実行しなさい」という意味
# url = yahoo_urlと書くことで、open_siteメソッドにyahoo_url変数に格納されている「https://yahoo.co.jp」というURLを渡している。








# 練習問題（ノーヒント）
# 問題
# 次の条件を満たすクラスを作成してください。
# 	1.	クラス名は SearchEngineManager とする。
# 	2.	以下の3つのメソッドを持たせること。
# 	•	get_browser_options: ブラウザのウィンドウサイズを指定する設定を作成して返す。
# 	•	start_browser: ブラウザを起動して返す。ログをprintで表示すること。
# 	•	open_search: 引数で受け取った検索エンジンのURLを開く。ログをprintで表示すること。
# 	3.	実行例では以下のように動作すること。
#  これからブラウザを起動します
# ブラウザを起動できました
# これから検索エンジンを開きます
# 検索エンジンを開きました: https://www.google.com
# 4.	最後に Google と Bing の2つのURLを用意し、クラスを使ってそれぞれのページを開くこと。
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class SearchEngineManager:
	def open_search(self, url):
		driver = self.start_browser()
		print(f"これから検索エンジンを開きます")
		driver.get(url)
		print(f"検索エンジンを開きました: {url}")

	def start_browser(self):
		service = Service()
		optns = self.get_browser_options()
		print(f"これからブラウザを起動します")
		driver = webdriver.Chrome(service=service, options=optns)
		print(f"ブラウザを起動できました")
		return driver

	def get_browser_options(self):
		optns = Options()
		optns.add_argument("--window-size=800,800")
		return optns

google_url ="https://www.google.com/"
bing_url ="https://www.bing.com/"

engine = SearchEngineManager()
engine.open_search(url = google_url)
    
    