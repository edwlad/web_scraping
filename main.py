from driver import WebDriverContext
from notik import Notik
# from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.by import By


sites = (Notik(),)

with WebDriverContext('', False) as driver:
    cnt = 1
    for site in sites:
        for url in site.urls:
            driver.get(url)
            # ActionChains(driver).pause(3).perform()
            for cnt, item in enumerate(site.items(driver), cnt):
                print(cnt, item)
