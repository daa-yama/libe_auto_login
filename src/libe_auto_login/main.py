from my_selenium import ChromeDriverManager

if __name__ == "__main__":
    driver = None
    try:
        driver = ChromeDriverManager().chrome_process()
        driver.get("https://example.com")
        input("Chromeが開いたらEnterを押してください → ")
    finally:
        if driver:
            driver.quit()