from selenium import webdriver


class WebDriverContext:
    """Контекст для открытия/закрытия браузера через вебдрайвер."""

    def __init__(self, name: str = 'chrome', head: bool = False):
        self.name = str(name).lower()
        self.head = bool(head)

    def __enter__(self):
        """Вход в контекст, ставит драйвер"""
        match self.name:
            case 'firefox':
                from selenium.webdriver.firefox.service import Service
                from selenium.webdriver.firefox.options import Options
                from webdriver_manager.firefox import GeckoDriverManager
                options = Options()
                options.headless = self.head
                # options.add_argument("--headless")
                # options.page_load_strategy = 'eager'
                # Отключение JS
                # options.set_preference('javascript.enabled', False)
                self.driver = webdriver.Firefox(
                    service=Service(GeckoDriverManager().install()),
                    options=options
                )
            case 'edge':
                from selenium.webdriver.edge.service import Service
                from selenium.webdriver.edge.options import Options
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                options = Options()
                options.headless = self.head
                # options.add_argument("--headless")
                # options.page_load_strategy = 'eager'
                # Отключение JS, images, CSS и т.д.
                # options.add_experimental_option(
                #     'prefs',
                #     {
                #         'profile.managed_default_content_settings.javascript': 2,
                #         'profile.managed_default_content_settings.images': 2,
                #         'profile.managed_default_content_settings.mixed_script': 2,
                #         'profile.managed_default_content_settings.media_stream': 2,
                #         'profile.managed_default_content_settings.stylesheets': 2
                #     }
                # )
                # Исключение вывода в консоль ошибки USB usb_device_handle_win.cc:... в Windows 10 для Chrome
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                self.driver = webdriver.Edge(
                    service=Service(EdgeChromiumDriverManager().install()),
                    options=options
                )
            case 'chrome' | _:
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.chrome.options import Options
                from webdriver_manager.chrome import ChromeDriverManager
                options = Options()
                options.headless = self.head
                # options.page_load_strategy = 'eager'
                # options.add_argument("--headless")
                # options.add_argument("--disable-dev-shm-usage")
                # options.add_argument("--no-sandbox")
                # Отключение JS, images, CSS и т.д.
                # options.add_experimental_option(
                #     'prefs',
                #     {
                #         'profile.managed_default_content_settings.javascript': 2,
                #         'profile.managed_default_content_settings.images': 2,
                #         'profile.managed_default_content_settings.mixed_script': 2,
                #         'profile.managed_default_content_settings.media_stream': 2,
                #         'profile.managed_default_content_settings.stylesheets': 2
                #     }
                # )
                # Исключение вывода в консоль ошибки USB usb_device_handle_win.cc:... в Windows 10 для Chrome
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    chrome_options=options
                )

        # Работа с cookies, но только после открытия страницы
        # self.driver.get(self.start_url)
        # cookies_list = self.driver.get_cookies()
        # self.cookies_dict = {}
        # for cookie in cookies_list:
        #     self.cookies_dict[cookie["name"]] = cookie["value"]

        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекста, завершает сессию общения с браузером."""
        self.driver.quit()
        if exc_type is not None:
            print(f"{exc_type}: {exc_val}; Traceback: {exc_val}")
