from typing import Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class InventoryPage:
    def __init__(self, driver: WebDriver):
        """
        Initializes the InventoryPage class with locators and a WebDriver instance.

        :param driver: Instance of the Selenium WebDriver.
        """
        self.driver = driver
        self.filter_dropdown: Tuple[str, str] = (
            By.CLASS_NAME,
            "product_sort_container",
        )
        self.cart_icon: Tuple[str, str] = (By.CLASS_NAME, "shopping_cart_badge")

    def sort_items_by_price(self, order: str = "low_to_high") -> None:
        """
        Sorts items on the inventory page by price.

        :param order: Sorting order. Accepted values are "low_to_high" or "high_to_low".
        :raises KeyError: If an invalid order is passed.
        """
        dropdown: WebElement = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.filter_dropdown)
        )
        filter_value: str = {"low_to_high": "lohi", "high_to_low": "hilo"}[order]
        dropdown.click()
        self.driver.find_element(
            By.CSS_SELECTOR, f"option[value='{filter_value}']"
        ).click()

    def add_item_to_cart(self, item_name: str) -> None:
        """
        Adds an item to the cart by its name.

        :param item_name: The name of the item to be added to the cart.
        """
        add_button: WebElement = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button",
                )
            )
        )
        add_button.click()

    def get_cart_count(self) -> int:
        """
        Retrieves the number of items in the cart by checking the cart icon badge.

        :return: Integer count of items in the cart. Returns 0 if no badge is visible.
        """
        try:
            cart_badge: WebElement = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located(self.cart_icon)
            )
            return int(cart_badge.text)
        except TimeoutException:
            return 0

    def navigate_to_product_details(self, item_name: str) -> None:
        """
        Navigates to the product details page for a specified item.

        :param item_name: The name of the item to navigate to.
        """
        product: WebElement = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, f"//div[text()='{item_name}']"))
        )
        product.click()
