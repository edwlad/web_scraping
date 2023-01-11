from selenium import webdriver


class WebDriverContext:
    """Контекст для открытия/закрытия браузера через вебдрайвер."""

    def __init__(self, name: str = 'chrome'):
        self.name = name.lower()

    def __enter__(self):
        """Вход в контекст, ставит драйвер"""
        match self.name:
            case 'firefox':
                from selenium.webdriver.firefox.service import Service
                from selenium.webdriver.firefox.options import Options
                from webdriver_manager.firefox import GeckoDriverManager
                options = Options()
                # options.headless = True
                # options.add_argument("--headless")
                self.driver = webdriver.Firefox(
                    service=Service(GeckoDriverManager().install()),
                    options=options
                )
            case 'edge':
                from selenium.webdriver.edge.service import Service
                from selenium.webdriver.edge.options import Options
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                options = Options()
                # options.headless = True
                # options.add_argument("--headless")
                self.driver = webdriver.Edge(
                    service=Service(EdgeChromiumDriverManager().install()),
                    options=options
                )
            case 'chrome' | _:
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.chrome.options import Options
                from webdriver_manager.chrome import ChromeDriverManager
                options = Options()
                # options.headless = True
                # options.add_argument("--headless")
                # options.add_argument("--disable-dev-shm-usage")
                # options.add_argument("--no-sandbox")
                # Исключение вывода в консоль ошибки USB usb_device_handle_win.cc:... в Windows 10 для Chrome
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    chrome_options=options
                )
        return self.driver
    
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--no-sandbox")
    #     chrome_options.add_argument("--disable-dev-shm-usage")
    #     # display = Display(visible=0, size=(800, 800))
    #     # display.start()
    #     self.driver = webdriver.Chrome(
    #         ChromeDriverManager().install(), chrome_options=chrome_options
    #     )
    #     self.driver.get(self.start_url)
    #     cookies_list = self.driver.get_cookies()
    #     self.cookies_dict = {}
    #     for cookie in cookies_list:
    #         self.cookies_dict[cookie["name"]] = cookie["value"]
    #     return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекста, завершает сессию общения с браузером."""
        self.driver.quit()
        if exc_type is not None:
            print(f"{exc_type}: {exc_val}; Traceback: {exc_val}")
