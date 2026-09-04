from selenium.webdriver.common.by import By
from pages.abstract_page import AbstractPage

class DashboardPage(AbstractPage):

    def __init__(self, driver):
        super().__init__(driver)

    def is_visible(self):
        return self.is_displayed(By.ID, "appContainer")

    def is_sidebar_visible(self):
        return self.is_displayed(By.CLASS_NAME, "sidebar")

    def navigate_to(self, page):
        self.click(By.CSS_SELECTOR, f"[data-page='{page}']")
        self.wait(0.5)

    def get_active_nav_item(self):
        return self.find_element(
            By.CSS_SELECTOR, ".nav-item.active"
        ).get_attribute("data-page")

    def get_page_title(self):
        return self.get_text(By.ID, "pageTitle")

    def is_nav_item_visible(self, page):
        return self.is_displayed(By.CSS_SELECTOR, f"[data-page='{page}']")

    def logout(self):
        self.click(By.CLASS_NAME, "logout-btn")
        self.wait(0.5)

    def search(self, text):
        self.type_text(By.CSS_SELECTOR, "input[placeholder*='Search']", text)
        self.wait(0.5)

    def refresh_data(self):
        self.click(By.CLASS_NAME, "btn-refresh")
        self.wait(1)

    def get_theme(self):
        return self.driver.execute_script(
            "return document.documentElement.getAttribute('data-theme')"
        )

    def set_theme(self, theme):
        self.driver.execute_script(f"setTheme('{theme}')")
        self.wait(0.5)

    def is_crypto_table_visible(self):
        return self.is_displayed(By.ID, "cryptoTableBody")

    def get_page_header_text(self):
        return self.get_text(By.CLASS_NAME, "top-bar")