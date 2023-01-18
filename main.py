from driver import WebDriverContext
from sqllite import Sqllite
from notik import Notik
from citilink_new import Citilink

# Параметры
browser = ('chrome', 'firefox', 'edge')[0]  # Выбор браузера
headless = True  # Не показывать окно браузера
max_items = 600  # Максимальное количество записей
new_data = True  # Заново собрать данные с сайтов
ranks = (('cpu_hhz', 2), ('ram_gb', 5), ('ssd_gb', 0.1), ('price_rub', -0.001))  # Рейтинг параметров
new_rank = False  # Пересчитать рейтинг
top = 5  # Количество лучших по рейтингу для вывода

sites = (Notik(), Citilink(),)
# sites = (Citilink(),)
with Sqllite() as db:
    # Сбор данных с сайтов
    if new_data:
        cnt = 0
        data = []
        db.create()

        for site in sites:
            if cnt >= max_items:
                break

            print('\n' + site.urls[0])
            with WebDriverContext(browser, headless) as driver:
                for item in site.items(driver):
                    cnt += 1
                    print('.', end='')
                    item['rank'] = sum(float(item[k]) * v for k, v in ranks)
                    data.append(item)
                    if cnt >= max_items:
                        break
                    if len(data) >= 50:
                        print(' ', cnt)
                        db.insert(data)
                        data.clear()

        print(' ', cnt)
        db.insert(data)
        data.clear()

    # Обновление рейтинга
    if not new_data and new_rank:
        db.update_rank(ranks)

    # Вывод топ рейтинга
    for row in db.top_list(top):
        print(
            f"Имя: {row['name']}\n"
            f"Процессор: {row['cpu_hhz']} ГГц; Память: {row['ram_gb']} ГБ; Диск: {row['ssd_gb']} ГБ\n"
            f"Рейтинг: {int(row['rank'])}; Цена: {row['price_rub']} р.; Дата: {row['visited_at']}\n"
            f"Ссылка: {row['url']}\n"
        )
