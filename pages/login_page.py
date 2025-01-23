from typing import Tuple

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    def __init__(self, driver: WebDriver):
        """
        Initializes the LoginPage class with locators and a WebDriver instance.

        :param driver: Instance of the Selenium WebDriver.
        """
        self.driver = driver
        self.username_field: Tuple[str, str] = (By.ID, "user-name")
        self.password_field: Tuple[str, str] = (By.ID, "password")
        self.login_button: Tuple[str, str] = (By.ID, "login-button")
        self.menu_button: Tuple[str, str] = (By.ID, "react-burger-menu-btn")
        self.logout_button: Tuple[str, str] = (By.ID, "logout_sidebar_link")
        self.error_message: Tuple[str, str] = (
            By.CSS_SELECTOR,
            "h3[data-test='error']",
        )

    def login(self, username: str, password: str) -> None:
        """
        Performs the login action by entering credentials and clicking the login button.

        :param username: Username to log in.
        :param password: Password to log in.
        """
        self.driver.find_element(*self.username_field).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def validate_error_message(self, expected_message: str) -> None:
        """
        Validates the error message displayed on unsuccessful login attempts.

        :param expected_message: The expected error message.
        :raises AssertionError: If the actual error message does not match the expected one.
        """
        error_text: str = (
            WebDriverWait(self.driver, 10)
            .until(ec.visibility_of_element_located(self.error_message))
            .text
        )
        assert error_text == expected_message, (
            f"Expected: {expected_message}, Got: {error_text}"
        )

    def verify_redirect_to_inventory(self) -> None:
        """
        Verifies that the user is redirected to the inventory page after a successful login.

        :raises AssertionError: If the current URL does not contain '/inventory.html'.
        """
        WebDriverWait(self.driver, 10).until(ec.url_contains("/inventory.html"))
        assert "/inventory.html" in self.driver.current_url, (
            "Failed to redirect to Inventory page."
        )

    def logout(self) -> None:
        """
        Logs out the user by clicking the menu button and the logout option.
        Verifies redirection back to the login page.

        :raises AssertionError: If the user is not redirected to the login page.
        """
        self.driver.find_element(*self.menu_button).click()
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.logout_button)
        ).click()

        WebDriverWait(self.driver, 10).until(
            ec.url_to_be("https://www.saucedemo.com/")
        )
        assert self.driver.current_url == "https://www.saucedemo.com/", (
            "Logout failed."
        )
