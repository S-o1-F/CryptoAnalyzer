import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://localhost:3000"

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def dashboard_page(driver):
    return DashboardPage(driver)


# za login

def test_login_page_loads(login_page):
    assert login_page.is_login_screen_visible()

def test_login_with_valid_credentials(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    assert dashboard_page.is_visible()

def test_login_screen_hidden_after_login(driver):
    login_page = LoginPage(driver)
    login_page.login("test@test.com", "password123")
    assert not login_page.is_login_screen_visible()

def test_login_empty_password_prevented(driver, login_page):
    login_page.enter_email("test@test.com")
    login_page.click_login()
    assert login_page.is_login_screen_visible()

# za language switch

def test_language_switch_to_macedonian(login_page):
    login_page.click_language("mk")
    assert login_page.get_login_button_text() == "Најава"

def test_language_switch_back_to_english(login_page):
    login_page.click_language("mk")
    login_page.click_language("en")
    assert login_page.get_login_button_text() == "Login"

#za navigation

def test_sidebar_visible_after_login(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    assert dashboard_page.is_sidebar_visible()

def test_navigate_to_sentiment(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("sentiment")
    assert dashboard_page.get_active_nav_item() == "sentiment"

def test_navigate_to_technical(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("technical")
    assert dashboard_page.get_active_nav_item() == "technical"

def test_navigate_to_prediction(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("predict")
    assert dashboard_page.get_active_nav_item() == "predict"

def test_navigate_to_portfolio(driver):
    #navigate to favorites
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("portfolio")
    assert dashboard_page.get_active_nav_item() == "portfolio"

def test_navigate_to_history(driver):
    """Test clicking History in sidebar"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("history")
    assert dashboard_page.get_active_nav_item() == "history"

def test_navigate_to_onchain(driver):
    """Test clicking On-Chain Metrics in sidebar"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("onchain")
    assert dashboard_page.get_active_nav_item() == "onchain"

def test_navigate_to_settings(driver):
    """Test clicking Settings in sidebar"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("settings")
    assert dashboard_page.get_active_nav_item() == "settings"


#za theme

def test_dark_theme_applied(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.set_theme("dark")
    assert dashboard_page.get_theme() == "dark"

def test_light_theme_applied(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.set_theme("dark")
    dashboard_page.set_theme("light")
    assert dashboard_page.get_theme() == "light"

# za logout

def test_logout_returns_to_login(driver):
    login_page = LoginPage(driver)
    login_page.login("test@test.com", "password123")
    driver.execute_script("logout()")
    import time
    time.sleep(0.5)
    assert login_page.is_login_screen_visible()

def test_app_hidden_after_logout(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    driver.execute_script("logout()")
    import time
    time.sleep(0.5)
    assert not dashboard_page.is_visible()

# za page title
def test_page_title_changes_to_sentiment(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("sentiment")
    assert dashboard_page.get_page_title() == "Sentiment Analysis"

def test_page_title_changes_to_technical(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")
    dashboard_page.navigate_to("technical")
    assert dashboard_page.get_page_title() == "Technical Analysis"


#levo sidebar dali e visible
def test_all_nav_items_visible(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.login("test@test.com", "password123")

    pages = ["dashboard", "portfolio", "predict",
             "history", "technical", "onchain",
             "sentiment", "settings"]

    for page in pages:
        assert dashboard_page.is_nav_item_visible(page), \
            f"Nav item '{page}' is not visible"