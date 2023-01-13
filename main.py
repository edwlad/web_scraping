from driver import WebDriverContext
from sqllite import Sqllite
from notik import Notik
from citilink import Citilink

browser = ('chrome', 'firefox', 'edge')[0]  # Выбор браузера
headless = False  # Не показывать окно браузера
max_items = 25  # Максимальное количество записей
new_data = True  # Заново собрать данные с сайтов
rank = {}  # Рейтинг параметров

sites = (Notik(), Citilink())

with Sqllite() as db:
    # Сбор данных с сайтов
    if new_data:
        db.create()
        with WebDriverContext(browser, headless) as driver:
            cnt = 1
            for site in sites:
                data = []
                for cnt, item in enumerate(site.items(driver), cnt):
                    # print(cnt, item)
                    data.append(item)
                    if cnt % 10 == 0:
                        db.insert(data)
                        data.clear()
                    if cnt >= max_items:
                        db.insert(data)
                        data.clear()
                        break
                else:
                    continue
                break
    
    # Обновление рейтинга