import json

from bs4 import BeautifulSoup
import requests
import time
import threading
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class RepeatedTimer(object):
    def __init__(self, interval, function, *args):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def alivetxt():
    headers = {
        "Authorization": 'Bearer ' + 'YEoQ6bGyN52EjmVh36uXxlRCiR7BNfdMluLWuTorlc7',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"message": 'I am alive'}

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)


def rent():
    multiRoom = 3
    price_min = 30000
    price_max = 45000
    url_dict = {
        "台北市": "https://rent.591.com.tw/?kind=1&option=cold&other=near_subway&region=1",
        "新北市": "https://rent.591.com.tw/?kind=1&option=cold&other=near_subway&region=3",
        # "桃園市": "https://rent.591.com.tw/?other=near_subway&region=6"
    }
    "https://rent.591.com.tw/?kind=1&option=cold&other=near_subway&multiRoom=3"
    filter_query = '&multiRoom='+str(multiRoom)+'&rentprice='+str(price_min)+','+str(price_max)+'&order=posttime&orderType=desc'

    Tempdata = []
    RepeatedTimer(14400, alivetxt)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)'
    }

    while True:
        try:
            # driver = webdriver.Chrome()
            d = DesiredCapabilities.CHROME
            d['goog:loggingPrefs'] = {'performance': 'ALL', 'network': 'ALL'}
            options = Options()
            # options.add_experimental_option('w3c', False)
            # 隐藏 正在受到軟體控制 這幾個字
            options.add_argument("disable-infobars")
            # logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
            # logger.setLevel(logging.WARNING)  # or any variant from ERROR, CRITICAL or NOTSET
            options.add_argument("--log-level=50")
            options.add_argument('--disable-logging')
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument('--headless')
            driver = webdriver.Chrome(ChromeDriverManager(print_first_line=False).install(), desired_capabilities=d, options=options)

            Newdata = []
            try:
                for region in url_dict:
                    url = url_dict[region] + filter_query
                    print(url)
                    print(region)
                    driver.get(url)
                    WebDriverWait(driver, 10)
                    time.sleep(5)
                    items = driver.find_elements(by=By.CSS_SELECTOR, value=".vue-list-rent-item")
                    for item in items:
                        # print(item)
                        # href = driver.create_web_element(item["ELEMENT"]).find_element(by=By.CSS_SELECTOR, value="a").get_property("href")
                        # text = driver.create_web_element(item["ELEMENT"]).find_element(by=By.CSS_SELECTOR, value=".item-title").text
                        href = item.find_element(by=By.CSS_SELECTOR, value="a").get_property("href")
                        text = item.find_element(by=By.CSS_SELECTOR, value=".item-title").text
                        price = item.find_element(by=By.CSS_SELECTOR, value=".item-price-text span").text
                        # print(text)
                        # print(href)
                        # print(div)
                        Newdata.append({
                            "region": region,
                            "text": text,
                            "href": href,
                            "price": price
                        })
            finally:
                driver.quit()

            # print(Newdata)
            list_difference = [item for item in Newdata if item not in Tempdata]
            payload = [i["region"]+' '+str(multiRoom)+'房 '+str(price_min)+'-'+str(price_max)+' 有新房喔 ' + i["text"] + ' $'+ i["price"] +' : 網址連結: https:' + i["href"] for i in list_difference]


            Tempdata = Newdata

            if list_difference and Tempdata:
                headers = {
                    "Authorization": 'Bearer ' + 'YEoQ6bGyN52EjmVh36uXxlRCiR7BNfdMluLWuTorlc7',
                    "Content-Type": "application/x-www-form-urlencoded"
                }

                for i in payload:
                    params = {"message": i}

                    r = requests.post("https://notify-api.line.me/api/notify",
                                      headers=headers, params=params)

            time.sleep(300)

        except Exception as e:
            print("Exception " + str(e))
            headers = {
                "Authorization": 'Bearer ' + 'YEoQ6bGyN52EjmVh36uXxlRCiR7BNfdMluLWuTorlc7',
                "Content-Type": "application/x-www-form-urlencoded"
            }
            params = {"message": 'Reboot'}

            r = requests.post("https://notify-api.line.me/api/notify",
                              headers=headers, params=params)
            time.sleep(5)


if __name__ == '__main__':
    rent()
