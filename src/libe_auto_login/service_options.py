from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class ChromeManager:

	def open_site(self, url):
		chrome = self.start_chrome()
		print(f"これからサイトを立ち上げます")
		chrome.get(url)
		print(f"これからサイトを立ち上げました{url}")
	
	def start_chrome(self):
		service = Service()
		chrome_options = self.get_chrome_options()
		print(f"これからブラウザを起動します")
		chrome = webdriver.Chrome(service=service, options=chrome_options)
		print(f"ブラウザを起動できました")
		return chrome

	def get_chrome_options(self):
		chrome_options = Options()
		chrome_options.add_argument("--window-size=840,600")
		return chrome_options

libe_url = "https://libecity.com"
yahoo_url = "https://yahoo.co.jp"
chrome_manager = ChromeManager()
# chrome_manager.open_site(url=libe_url)
chrome_manager.open_site(url=yahoo_url)