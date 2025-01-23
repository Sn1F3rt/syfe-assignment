from typing import Tuple

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class CheckoutPage:
    def __init__(self, driver: WebDriver):
        """
        Initializes the CheckoutPage class with locators and a WebDriver instance.

        :param driver: Instance of the Selenium WebDriver.
        """
        self.driver = driver
        self.first_name_field: Tuple[str, str] = (By.ID, "first-name")
        self.last_name_field: Tuple[str, str] = (By.ID, "last-name")
        self.postal_code_field: Tuple[str, str] = (By.ID, "postal-code")
        self.continue_button: Tuple[str, str] = (By.ID, "continue")
        self.finish_button: Tuple[str, str] = (By.ID, "finish")
        self.success_message: Tuple[str, str] = (By.CLASS_NAME, "complete-header")

    def fill_checkout_form(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        """
        Fills out the checkout form with the provided information.

        :param first_name: Customer's first name.
        :param last_name: Customer's last name.
        :param postal_code: Customer's postal code.
        """
        self.driver.find_element(*self.first_name_field).send_keys(first_name)
        self.driver.find_element(*self.last_name_field).send_keys(last_name)
        self.driver.find_element(*self.postal_code_field).send_keys(postal_code)
        self.driver.find_element(*self.continue_button).click()

    def complete_purchase(self) -> None:
        """
        Completes the purchase by clicking the "Finish" button.
        """
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.finish_button)
        ).click()

    def verify_success_message(self) -> None:
        """
        Verifies that the success message is displayed after completing the purchase.

        :raises AssertionError: If the success message does not match the expected text.
        """
        success_text: str = (
            WebDriverWait(self.driver, 10)
            .until(ec.visibility_of_element_located(self.success_message))
            .text
        )
        assert success_text == "Thank you for your order!", (
            "Success message mismatch."
        )
