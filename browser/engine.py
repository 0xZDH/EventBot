#!/usr/bin/env python

from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options

class BrowserEngine:

    options = Options()
    profile = FirefoxProfile() # Set certain preferences at a class level as they are static
    profile.accept_untrusted_certs = True
    profile.set_preference('permissions.default.image', 2) # Supposed to help with memory issues
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)

    def __init__(self, wait, proxy=None, headless=False):
        self.proxy = None if not proxy else self.set_proxy(proxy)
        self.options.headless = headless
        self.driver = Firefox(options=self.options, firefox_profile=self.profile, proxy=self.proxy)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, 768)
        self.wait = WebDriverWait(self.driver, wait)

    def set_proxy(self, proxy):
        return Proxy({
            "proxyType": ProxyType.MANUAL,
            "httpProxy": proxy,
            "ftpProxy":  proxy,
            "sslProxy":  proxy,
            "noProxy":   ""
        })

    def quit_driver(self):
        self.driver.quit()

    def refresh(self):
        self.driver.refresh()

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def get_request(self, url):
        self.driver.get(url)

    def get_element(self, type_, value):
        try:
            return self.wait.until(
                lambda driver: driver.find_element(
                    getattr(By, type_), value)
                )
        except TimeoutException:
            return False

    def click_button(self, button):
        button.click()

    def select_dropdown(self, element, value):
        select = Select(element)
        select.select_by_value(value)

    def switch_context(self, element):
        self.driver.switch_to.frame(element)