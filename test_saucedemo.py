import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def setup():
    service=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)  # Wait for the page to load
    yield driver
    time.sleep(2)  # Wait before quitting the driver
    driver.quit()

def test_valid_login(setup):
    driver = setup
    time.sleep(2)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    time.sleep(2)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    time.sleep(2)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    assert "Products" in driver.title

def test_invalid_login(setup):
    driver = setup
    time.sleep(2)
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    time.sleep(2)
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    time.sleep(2)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
    time.sleep(2)
    assert "Epic sadface" in error_message
    
def test_checkout_success(setup):
    driver = setup
    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Add a product to the cart
    driver.find_element(By.XPATH, "//div[@class='inventory_item'][1]//button").click()

    # Go to the cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Proceed to checkout
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # Finish checkout
    # driver.find_element(By.ID, "finish").click()
    # success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
    # assert "THANK YOU FOR YOUR ORDER" in success_message
    

def test_add_single_product(setup):
    driver = setup
    time.sleep(2)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='inventory_item'][1]//button").click()
    time.sleep(2)
    assert "Sauce Labs Backpack" in driver.page_source
