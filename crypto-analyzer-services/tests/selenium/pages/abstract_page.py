from selenium.webdriver.common.by import By
import time


class AbstractPage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def click(self, by, value):
        self.driver.find_element(by, value).click()

    def type_text(self, by, value, text):
        element = self.driver.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def is_displayed(self, by, value):
        return self.driver.find_element(by, value).is_displayed()

    def get_text(self, by, value):
        return self.driver.find_element(by, value).text

    def wait(self, seconds=0.5):
        time.sleep(seconds)

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url