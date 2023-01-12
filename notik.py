from selenium import webdriver
from selenium.webdriver import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime


class Notik():
    def __init__(self):
        # self.urls = ('file://c:/Www/git/web_scraping/temp_notik.html',)
        self.urls = (
            'https://www.notik.ru/search_catalog/filter/work.htm',
            'https://www.notik.ru/search_catalog/filter/home.htm',
            'https://www.notik.ru/search_catalog/filter/universal.htm',
            'https://www.notik.ru/search_catalog/filter/base.htm',
            'https://www.notik.ru/search_catalog/filter/mobile.htm',
            'https://www.notik.ru/search_catalog/filter/ultrabooks.htm',
            'https://www.notik.ru/search_catalog/filter/ultrabook-transformer.htm',
        )

    def items(self, driver: webdriver.Chrome):
        pages = [None]
        paginator = driver.find_elements(By.CLASS_NAME, 'paginator')
        if paginator:
            pages.extend([
                v.get_attribute('href')
                for v in paginator[0].find_elements(By.TAG_NAME, 'a')[1:]
            ])

        for page in pages:
            if page is not None:
                driver.get(page)

            ActionChains(driver).pause(2).perform()
            for item in driver.find_elements(By.CSS_SELECTOR, '.goods-list-grouped-table .goods-list-table'):
                tds = item.find_elements(By.TAG_NAME, 'td')
                ram_ssd = tds[2].text.split()
                out = {
                    'cpu_hhz': int(tds[1].text.rsplit(None, 2)[-2]) / 1000,
                    'ram_gb': int(ram_ssd[0]),
                    'ssd_gb': int(ram_ssd[-2]),
                    'price_rub': tds[7].find_element(By.TAG_NAME, 'a').get_attribute('ecprice'),
                    'name': tds[7].find_element(By.TAG_NAME, 'a').get_attribute('ecname'),
                    'url': tds[0].find_element(By.TAG_NAME, 'a').get_attribute('href'),
                    'visited_at': str(datetime.today())[:19],
                }

                yield out
