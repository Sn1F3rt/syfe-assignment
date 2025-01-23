from typing import Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class ProductDetailsPage:
    def __init__(self, driver: WebDriver):
        """
        Initializes the ProductDetailsPage class with locators and a WebDriver instance.

        :param driver: Instance of the Selenium WebDriver.
        """
        self.driver = driver
        self.add_to_cart_button: Tuple[str, str] = (By.CLASS_NAME, "btn_inventory")
        self.cart_icon: Tuple[str, str] = (By.CLASS_NAME, "shopping_cart_badge")

    def add_to_cart(self) -> None:
        """
        Adds the product displayed on the product details page to the cart.

        :raises TimeoutException: If the add-to-cart button is not clickable within the wait time.
        """
        add_button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.add_to_cart_button)
        )
        add_button.click()

    def get_cart_count(self) -> int:
        """
        Retrieves the number of items in the cart by checking the cart icon badge.

        :return: Integer count of items in the cart. Returns 0 if the cart badge is not visible.
        :raises TimeoutException: If the cart badge is not found within the wait time.
        """
        try:
            cart_badge = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located(self.cart_icon)
            )
            return int(cart_badge.text)
        except TimeoutException:
            return 0
