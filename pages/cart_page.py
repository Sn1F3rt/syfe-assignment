from typing import List, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class CartPage:
    def __init__(self, driver: WebDriver):
        """
        Initializes the CartPage class with locators and a WebDriver instance.

        :param driver: Instance of the Selenium WebDriver.
        """
        self.driver = driver
        self.cart_items: Tuple[str, str] = (By.CLASS_NAME, "cart_item")
        self.cart_icon: Tuple[str, str] = (By.CLASS_NAME, "shopping_cart_badge")
        self.checkout_button: Tuple[str, str] = (By.ID, "checkout")
        self.remove_button_template: Tuple[str, str] = (
            By.XPATH,
            "//div[contains(text(),'{item_name}')]/ancestor::div[@class='cart_item']//button",
        )
        self.item_price: Tuple[str, str] = (By.CLASS_NAME, "inventory_item_price")
        self.remove_buttons: Tuple[str, str] = (By.CLASS_NAME, "cart_button")

    def get_cart_count(self) -> int:
        """
        Retrieves the number of items currently in the cart by checking the cart icon badge.

        :return: Integer count of items in the cart. Returns 0 if no badge is visible.
        """
        try:
            cart_badge: WebElement = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located(self.cart_icon)
            )
            return int(cart_badge.text)
        except TimeoutException:
            return 0

    def remove_item_by_price_range(self, min_price: float, max_price: float) -> None:
        """
        Removes the first item in the cart whose price falls within the specified range.

        :param min_price: Minimum price of the item to be removed.
        :param max_price: Maximum price of the item to be removed.
        """
        items: List[WebElement] = self.driver.find_elements(*self.cart_items)
        for item in items:
            price_text: str = item.find_element(*self.item_price).text.strip("$")
            price: float = float(price_text)
            if min_price <= price <= max_price:
                item.find_element(*self.remove_buttons).click()
                break

    def click_checkout(self) -> None:
        """
        Proceeds to the checkout page by clicking the checkout button.
        """
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.checkout_button)
        ).click()
