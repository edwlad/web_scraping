from selenium import webdriver
from selenium.webdriver import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
import re


class Citilink():
    def __init__(self):
        self.urls = ('https://www.citilink.ru/catalog/noutbuki/?view_type=list&f=available.all',)

    def items(self, driver: webdriver.Chrome):
        # driver.implicitly_wait(5)
        for url in self.urls:
            next_page = url

            while next_page:
                driver.get(next_page)
                ActionChains(driver).pause(2).perform()

                for item in driver.find_elements(By.XPATH, '//*[contains(text(), "Экран")]/ancestor::div[2]'):
                    head = item.find_element(By.XPATH, './div[3]//a')
                    props = item.text
                    cpu_hhz = re.search(r'Процессор.+?ГГц', props)
                    ram_gb = re.search(r'память.+?ГБ', props)
                    ssd_gb = re.search(r'(Диск|Объем).+?ГБ', props)
                    price = re.search(r'[\d]+(?=₽)', props.replace(' ', ''))
                    out = {
                        'cpu_hhz': float(cpu_hhz[0].split()[-2]) if cpu_hhz else 0.0,
                        'ram_gb': int(ram_gb[0].split()[-2]) if ram_gb else 0,
                        'ssd_gb': int(ssd_gb[0].split()[-2]) if ssd_gb else 0,
                        'price_rub': int(price[0] if price else 0),
                        'name': head.text,
                        'url': head.get_attribute('href'),
                        'visited_at': str(datetime.today())[:19],
                    }
                    # price item.text.replace(' ', '').split()
                    yield out

                next_page = driver.find_elements(By.XPATH, '//*[contains(text(), "Следующая")]/ancestor::a[1]')
                if next_page:
                    next_page = next_page[0].get_attribute('href')

        return
