from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_login_and_check_element():

    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f'{host}/login')

        # Wait a little while to make sure the page has loaded completely
        time.sleep(4)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')

        email_field.send_keys('user1@example.com')
        password_field.send_keys('1234')

        # Send the form
        password_field.send_keys(Keys.RETURN)

        # Wait a little while to ensure that the action has been completed
        time.sleep(4)

        try:

            driver.find_element(By.XPATH, "//h1[contains(@class, 'h2 mb-3') and contains(., 'Latest datasets')]")
            print('Test passed!')

        except NoSuchElementException:
            raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)


def test_remember_my_password():

    driver = initialize_driver()

    driver.get("http://localhost:5000/remember-my-password")
    driver.set_window_size(840, 813)
    driver.find_element(By.LINK_TEXT, "Login").click()
    driver.find_element(By.LINK_TEXT, "Remember my password").click()
    driver.find_element(By.ID, "email").click()
    driver.find_element(By.ID, "email").send_keys("ho")
    driver.find_element(By.ID, "email").send_keys("user")
    driver.find_element(By.ID, "email").send_keys(Keys.DOWN)
    driver.find_element(By.ID, "email").send_keys("user1@example.com")
    driver.find_element(By.ID, "submit").click()


# Call the test function
test_login_and_check_element()
test_remember_my_password()
