# Домашнее задание по теме "Веб-скрапинг"

## Введение

Вы выбираете себе новый ноутбук для покупки. Вы овладели навыками работы с инструментами веб-скрапинга и вам не терпится их применить для решения этой задачи. Вы решаете собрать и сравнить ноутбуки с разных сайтов и выбрать из них лучший по вашему мнению. Вы решаете хранить собранные данные в таблице и автоматически выставлять к записям рейтинг "привлекательности для покупки"

## Требования

- Напишите скрапер собирающий информацию с сайтов на ваш выбор
- должно быть не менее **500 записей** о технике
- должны быть данные с **не менее чем 2 сайтов**
- должно быть складывание **в базу**
- дожно быть автоматическое **вычисление рейтинга** сразу
- напишите **readme.md** с кратким описанием инструкцией запуска
- используйте **requirements.txt** для указания сторонних зависимостей и их версий

## Реализация

### Ньюансы

17.01.2023 - Структура сайта Ситилинк иногда не сооветствует скрипту. Тогда данные с сайта не берутся.

### Используемые модули, структура

Для сбора данных выбраны два сайта [Notik](https://www.notik.ru/) и [Citilink](https://www.citilink.ru/).

Используются:

- Интерпретатор [Python v 3.10](https://www.python.org/).
- [Selenium 4](https://www.selenium.dev/) для автоматизации действий веб-браузера.
- [Webdriver-manager](https://pypi.org/project/webdriver-manager/) для автоматической загрузки актуальных веб-драйверов.
- База данных [SQLite-python](https://docs.python.org/3/library/sqlite3.html) для записи найденых данных.

Структура таблицы:

```SQL
CREATE TABLE <имя_таблицы> (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    url TEXT, -- ссылка на страницу товара  
    visited_at timestamp,  -- время посещения страницы  
    name TEXT,  -- наименование товара  
    cpu_hhz REAL,  -- частота процессора, ГГЦ  
    ram_gb INTEGER,  -- объем ОЗУ, Гб  
    ssd_gb INTEGER,  -- Объем SSD, Гб  
    price_rub INTEGER,  -- Цена, руб  
    rank REAL  -- вычисляемый рейтинг  
);
```

### Конфигурация, запуск

Конфигурация находится в файле [main.py](main.py) в секции ***# Параметры*** (указаны значения используемые по умолчанию):

```python
# Параметры
browser = ('chrome', 'firefox', 'edge')[0]  # Выбор браузера
headless = True  # Не показывать окно браузера
max_items = 600  # Максимальное количество записей
new_data = True  # Заново собрать данные с сайтов
ranks = (  # Рейтинг параметров
    ('cpu_hhz', 2),
    ('ram_gb', 5),
    ('ssd_gb', 0.1),
    ('price_rub', -0.001)
)
new_rank = False  # Пересчитать рейтинг
top = 5  # Количество лучших по рейтингу для вывода
```

Запуск - скрипт [main.py](main.py).

### Работа

При указанных параметрах запустится сбор данных с сайтов без открытия окна браузера. Ход работы отображается в консоли.

Собраны будут 600 записей. После завершения сбора, выведется информация о ТОП 5 лучших вариантов по рейтингу.

Вариант вывода (в примере длинные записи обрезаны):

```text
Имя: MSI Stealth GS77 12UHS-030RU i9-12900H 64Gb ...
Процессор: 2.5 ГГц; Память: 64 ГБ; Диск: 2048 ГБ
Рейтинг: 190; Цена: 338900 р.; Дата: 2023-01-13 21:59:13
Ссылка: https://www.notik.ru/goods/notebooks-msi- ...
```

### Описание некоторых настроек

`browser = ('chrome', 'firefox', 'edge')[0]` - в квадратных скобках указывается индекс используемого браузера:

- 0 - Chrome
- 1 - Firefox
- 2 - MS Edge

---

`new_data` - собирать или нет новые данные с сайтов:

- `True` - очистить базу, собирать **все записи заново** и вывести ТОП. Рейтинг посчитается при сборе. Настройка `new_rank` **не влияет** на расчет рейтинга.
- `False` - **не собирать** записи и вывести ТОП.

---

`new_rank` - пересчитать рейтинг или нет:

- `True` - персчитается рейтинг и изменится в базе данных. Пересчет будет проведен при условии что `new_data = False`.
- `False` - не персчитывать рейтинг.

---

`ranks` - список весов для параметров:

- `cpu_hhz` - вес частоты процессора
- `ram_gb` - вес объема памяти
- `ssd_gb` - вес ёмкости диска
- `price_rub` - вес цены

Пример записи весов:

```python
ranks = (
    ('cpu_hhz', 2),
    ('ram_gb', 5),
    ('ssd_gb', 0.1),
    ('price_rub', -0.001)
)
```

### Особенности

Данные по умолчанию собираются в файл базы данных [nout.db](nout.db).

В проекте есть два файла [nout.db](nout.db) и [nout_old.db](nout_old.db). В них уже есть собраная информация о 600 ноутбуках с сайтов. Если при запуске программы указана насторйка `new_data = False`, то будут использоваться данные из файла [nout.db](nout.db).

## Пример вывода ТОП 5

```text
Имя: MSI Stealth GS77 12UHS-030RU i9-12900H 64Gb SSD 2Tb NVIDIA RTX 3080Ti для ноутбуков 16Gb 17,3 UHD IPS Cam 99.9Вт*ч Win11 Черный 9S7-17P112-030
Процессор: 2.5 ГГц; Память: 64 ГБ; Диск: 2048 ГБ
Рейтинг: 190; Цена: 338900 р.; Дата: 2023-01-14 22:49:45
Ссылка: https://www.notik.ru/goods/notebooks-msi-stealth-gs77-12uhs-030ru-black-91481.htm

Имя: MSI CreatorPro X17 A12UKS-206RU i9-12900HX 64Gb SSD 2Tb NVIDIA RTX A3000 для ноутбуков 12Gb 17,3 UHD IPS Cam 99Вт*ч Win11Pro Черный 9S7-17Q121-206
Процессор: 2.3 ГГц; Память: 64 ГБ; Диск: 2048 ГБ
Рейтинг: 187; Цена: 341900 р.; Дата: 2023-01-14 22:49:03
Ссылка: https://www.notik.ru/goods/notebooks-msi-creatorpro-x17-a12uks-206ru-black-92336.htm

Имя: Acer Aspire A315-57G i7-1065G7 8Gb 2Tb NVIDIA MX330 2Gb 15,6 FHD Cam 36Вт*ч No OS Черный A315-57G-73F1 NX.HZRER.01M
Процессор: 1.3 ГГц; Память: 8 ГБ; Диск: 2000 ГБ
Рейтинг: 186; Цена: 55990 р.; Дата: 2023-01-14 22:50:08
Ссылка: https://www.notik.ru/goods/notebooks-acer-aspire-3-a315-57g-73f1-black-91236.htm

Имя: MSI Titan GT77 12UHS-208RU i9-12900HX 64Gb SSD 3Tb NVIDIA RTX 3080Ti для ноутбуков 16Gb 17,3 UHD IPS Cam 99Вт*ч Win11 Серый 9S7-17Q111-208
Процессор: 2.3 ГГц; Память: 64 ГБ; Диск: 3072 ГБ
Рейтинг: 185; Цена: 446400 р.; Дата: 2023-01-14 22:49:48
Ссылка: https://www.notik.ru/goods/notebooks-msi-titan-gt77-12uhs-208ru-black-91471.htm

Имя: Dream Machines G1650-15KZ84 i5-12500H 32Gb SSD 1Tb NVIDIA GTX1650 4Gb 15,6 FHD WVA Cam 62.32Вт*ч No OS KBD RUENG Черный G1650-15KZ84
Процессор: 2.5 ГГц; Память: 32 ГБ; Диск: 1024 ГБ
Рейтинг: 160; Цена: 106770 р.; Дата: 2023-01-14 22:49:58
Ссылка: https://www.notik.ru/goods/notebooks-dream-machines-g1650-15kz84-black-93654.htm
```
