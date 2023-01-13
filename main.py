from driver import WebDriverContext
from notik import Notik
from citilink import Citilink

browser = ('chrome', 'firefox', 'edge')[1]
headless = False
max_items = 600

sites = (Notik(), Citilink())

with WebDriverContext(browser, headless) as driver:
    cnt = 1
    for site in sites:
        for cnt, item in enumerate(site.items(driver), cnt):
            print(cnt, item)
            if cnt >= max_items:
                break
        else:
            continue
        break
