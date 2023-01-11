from driver import WebDriverContext
from selenium.webdriver import ActionChains

'''
from context import WebDriverContext
from page import OnePage
from config import START_URL, OUTPUT_PNG


with WebDriverContext(START_URL) as ctx:
    """Основной сценарий."""
    page = OnePage(ctx.driver)
    page.put_search_string("pep 8")
    page.click_search()
    ctx.driver.save_screenshot(OUTPUT_PNG)
'''

with WebDriverContext('-firefox') as drv:
    print(drv)
    drv.get('https://ya.ru')
    ActionChains(drv).pause(3).perform()
    