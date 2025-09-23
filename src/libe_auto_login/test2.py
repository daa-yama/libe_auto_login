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
    