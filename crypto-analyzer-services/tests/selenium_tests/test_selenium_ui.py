import pytest
import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.login("test@test.com", "password123")
    time.sleep(1)
    return driver

#za login
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


def test_language_switch_to_macedonian(login_page):
    login_page.click_language("mk")
    assert login_page.get_login_button_text() == "Најава"


def test_language_switch_back_to_english(login_page):
    login_page.click_language("mk")
    login_page.click_language("en")
    assert login_page.get_login_button_text() == "Login"

#za navigation

def test_sidebar_visible_after_login(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    assert dashboard_page.is_sidebar_visible()


def test_navigate_to_sentiment(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("sentiment")
    assert dashboard_page.get_active_nav_item() == "sentiment"


def test_navigate_to_technical(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("technical")
    assert dashboard_page.get_active_nav_item() == "technical"


def test_navigate_to_prediction(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("predict")
    assert dashboard_page.get_active_nav_item() == "predict"


def test_navigate_to_portfolio(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("portfolio")
    assert dashboard_page.get_active_nav_item() == "portfolio"


def test_navigate_to_history(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("history")
    assert dashboard_page.get_active_nav_item() == "history"


def test_navigate_to_onchain(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("onchain")
    assert dashboard_page.get_active_nav_item() == "onchain"


def test_navigate_to_settings(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    assert dashboard_page.get_active_nav_item() == "settings"


def test_all_nav_items_visible(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    pages = ["dashboard", "portfolio", "predict",
             "history", "technical", "onchain",
             "sentiment", "settings"]
    for page in pages:
        assert dashboard_page.is_nav_item_visible(page), \
            f"Nav item '{page}' is not visible"

#light/dark theme

def test_dark_theme_applied(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.set_theme("dark")
    assert dashboard_page.get_theme() == "dark"


def test_light_theme_applied(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.set_theme("dark")
    dashboard_page.set_theme("light")
    assert dashboard_page.get_theme() == "light"

#logout

def test_logout_returns_to_login(logged_in_driver):
    login_page = LoginPage(logged_in_driver)
    logged_in_driver.execute_script("logout()")
    time.sleep(0.5)
    assert login_page.is_login_screen_visible()


def test_app_hidden_after_logout(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    logged_in_driver.execute_script("logout()")
    time.sleep(0.5)
    assert not dashboard_page.is_visible()

#za page titles

def test_page_title_changes_to_sentiment(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("sentiment")
    assert dashboard_page.get_page_title() == "Sentiment Analysis"


def test_page_title_changes_to_technical(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("technical")
    assert dashboard_page.get_page_title() == "Technical Analysis"

#search bar

def test_search_bar_is_visible(logged_in_driver):
    search = logged_in_driver.find_element(By.ID, "globalSearch")
    assert search.is_displayed()


def test_search_bar_accepts_input(logged_in_driver):
    search = logged_in_driver.find_element(By.ID, "globalSearch")
    search.send_keys("BTC")
    assert search.get_attribute("value") == "BTC"


def test_search_shows_results(logged_in_driver):
    wait = WebDriverWait(logged_in_driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "cryptoTableBody")))
    time.sleep(2)
    search = logged_in_driver.find_element(By.ID, "globalSearch")
    search.send_keys("BTC")
    time.sleep(1)
    search_results = logged_in_driver.find_element(By.ID, "searchResults")
    assert search_results is not None

#refresh button

def test_refresh_button_is_visible(logged_in_driver):
    refresh_btn = logged_in_driver.find_element(By.CLASS_NAME, "btn-refresh")
    assert refresh_btn.is_displayed()


def test_refresh_button_is_clickable(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    refresh_btn = logged_in_driver.find_element(By.CLASS_NAME, "btn-refresh")
    refresh_btn.click()
    time.sleep(1)
    assert dashboard_page.is_visible()

#favorites

def test_portfolio_empty_message_visible(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    logged_in_driver.execute_script("localStorage.removeItem('cryptoWatchlist')")
    logged_in_driver.execute_script("watchlist = []")
    logged_in_driver.execute_script("updatePortfolioTable()")
    dashboard_page.navigate_to("portfolio")
    time.sleep(0.5)
    empty_msg = logged_in_driver.find_element(By.ID, "emptyPortfolio")
    assert empty_msg is not None


def test_add_and_remove_from_favorites(logged_in_driver):
    logged_in_driver.execute_script(
        "watchlist = ['BTCUSDT']; saveWatchlistToStorage(); updatePortfolioTable();"
    )
    time.sleep(0.5)
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("portfolio")
    time.sleep(0.5)
    portfolio_table = logged_in_driver.find_element(By.ID, "portfolioTableBody")
    assert "BTCUSDT" in portfolio_table.text or len(
        portfolio_table.find_elements(By.TAG_NAME, "tr")
    ) > 0
    logged_in_driver.execute_script("removeFromWatchlist('BTCUSDT')")
    time.sleep(0.5)
    empty_msg = logged_in_driver.find_element(By.ID, "emptyPortfolio")
    assert empty_msg.is_displayed()


def test_favorites_empty_after_removing_all(logged_in_driver):
    logged_in_driver.execute_script(
        "watchlist = ['BTCUSDT', 'ETHUSDT']; saveWatchlistToStorage(); updatePortfolioTable();"
    )
    time.sleep(0.5)
    logged_in_driver.execute_script("removeFromWatchlist('BTCUSDT')")
    logged_in_driver.execute_script("removeFromWatchlist('ETHUSDT')")
    time.sleep(0.5)
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("portfolio")
    time.sleep(0.5)
    empty_msg = logged_in_driver.find_element(By.ID, "emptyPortfolio")
    assert empty_msg.is_displayed()


#history

def test_history_page_has_crypto_select(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("history")
    time.sleep(1)
    selects = logged_in_driver.find_elements(By.TAG_NAME, "select")
    assert len(selects) > 0


#technical page

def test_technical_page_has_timeframe_select(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("technical")
    time.sleep(1)
    selects = logged_in_driver.find_elements(By.TAG_NAME, "select")
    assert len(selects) >= 2


#on-chain

def test_onchain_page_has_crypto_select(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("onchain")
    time.sleep(1)
    selects = logged_in_driver.find_elements(By.TAG_NAME, "select")
    assert len(selects) > 0


def test_onchain_active_addresses_element_exists(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("onchain")
    element = logged_in_driver.find_element(By.ID, "onchainActiveAddresses")
    assert element is not None


def test_onchain_transactions_element_exists(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("onchain")
    element = logged_in_driver.find_element(By.ID, "onchainTransactions")
    assert element is not None


#settings

def test_settings_profile_tab_is_active_by_default(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    active_tab = logged_in_driver.find_element(By.CSS_SELECTOR, ".settings-tab.active")
    assert active_tab.get_attribute("data-settings-tab") == "profile"


def test_settings_name_input_has_default_value(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    name_input = logged_in_driver.find_element(
        By.CSS_SELECTOR, ".settings-content input[type='text']"
    )
    assert name_input.get_attribute("value") != ""


def test_settings_name_input_can_be_changed(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    name_input = logged_in_driver.find_element(
        By.CSS_SELECTOR, ".settings-content input[type='text']"
    )
    name_input.clear()
    name_input.send_keys("SKIT")
    assert name_input.get_attribute("value") == "SKIT"


def test_settings_email_input_is_visible(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    email_input = logged_in_driver.find_element(
        By.CSS_SELECTOR, ".settings-content input[type='email']"
    )
    assert email_input.is_displayed()


def test_settings_email_input_can_be_changed(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    email_input = logged_in_driver.find_element(
        By.CSS_SELECTOR, ".settings-content input[type='email']"
    )
    email_input.clear()
    email_input.send_keys("SKIT@test.com")
    assert email_input.get_attribute("value") == "SKIT@test.com"


def test_notifications_tab_opens(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    logged_in_driver.find_element(
        By.CSS_SELECTOR, "[data-settings-tab='notifications']"
    ).click()
    time.sleep(0.5)
    notifications_content = logged_in_driver.find_element(By.ID, "settings-notifications")
    assert "active" in notifications_content.get_attribute("class")


def test_price_alerts_toggle_is_checked_by_default(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    logged_in_driver.find_element(
        By.CSS_SELECTOR, "[data-settings-tab='notifications']"
    ).click()
    time.sleep(0.5)
    toggles = logged_in_driver.find_elements(
        By.CSS_SELECTOR, "#settings-notifications input[type='checkbox']"
    )
    assert toggles[0].is_selected()


def test_portfolio_updates_toggle_is_checked_by_default(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    logged_in_driver.find_element(
        By.CSS_SELECTOR, "[data-settings-tab='notifications']"
    ).click()
    time.sleep(0.5)
    toggles = logged_in_driver.find_elements(
        By.CSS_SELECTOR, "#settings-notifications input[type='checkbox']"
    )
    assert toggles[1].is_selected()


def test_market_news_toggle_is_unchecked_by_default(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    logged_in_driver.find_element(
        By.CSS_SELECTOR, "[data-settings-tab='notifications']"
    ).click()
    time.sleep(0.5)
    toggles = logged_in_driver.find_elements(
        By.CSS_SELECTOR, "#settings-notifications input[type='checkbox']"
    )
    assert not toggles[2].is_selected()


def test_price_alerts_toggle_can_be_turned_off(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    logged_in_driver.find_element(
        By.CSS_SELECTOR, "[data-settings-tab='notifications']"
    ).click()
    time.sleep(0.5)
    toggles = logged_in_driver.find_elements(
        By.CSS_SELECTOR, "#settings-notifications input[type='checkbox']"
    )
    logged_in_driver.execute_script("arguments[0].click();", toggles[0])
    time.sleep(0.5)
    assert not toggles[0].is_selected()


def test_market_news_toggle_can_be_turned_on(logged_in_driver):
    dashboard_page = DashboardPage(logged_in_driver)
    dashboard_page.navigate_to("settings")
    logged_in_driver.find_element(
        By.CSS_SELECTOR, "[data-settings-tab='notifications']"
    ).click()
    time.sleep(0.5)
    toggles = logged_in_driver.find_elements(
        By.CSS_SELECTOR, "#settings-notifications input[type='checkbox']"
    )
    logged_in_driver.execute_script("arguments[0].click();", toggles[2])
    time.sleep(0.5)
    assert toggles[2].is_selected()

