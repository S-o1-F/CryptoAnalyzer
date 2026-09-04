from selenium.webdriver.common.by import By
from pages.abstract_page import AbstractPage

class LoginPage(AbstractPage):

    def __init__(self, driver):
        super().__init__(driver)

    def enter_email(self, email):
        self.type_text(By.ID, "loginEmail", email)

    def enter_password(self, password):
        self.type_text(By.ID, "loginPassword", password)

    def click_login(self):
        self.click(By.CLASS_NAME, "btn-login")
        self.wait(1)

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def get_alert_text(self):
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except:
            return None

    def is_login_screen_visible(self):
        return self.is_displayed(By.ID, "loginScreen")

    def click_language(self, lang):
        self.click(By.CSS_SELECTOR, f"[data-lang='{lang}']")
        self.wait(0.5)

    def get_login_button_text(self):
        return self.get_text(By.CLASS_NAME, "btn-login")