from pages.cart_page import CartPage
from utils.base_test import BaseTest
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.product_details_page import ProductDetailsPage


class Test(BaseTest):
    """
    A test class that performs end-to-end tests for the SauceDemo website using Selenium.
    Inherits from BaseTest to handle WebDriver setup and teardown.
    """

    def test(self) -> None:
        """
        Executes the full end-to-end test scenario covering login, inventory actions, cart management,
        checkout, and logout.
        """
        self.setup()

        try:
            # Task 1: Login Validation
            login_page = LoginPage(self.driver)
            login_page.login(
                "standard_user", "secret_sauce"
            )  # Logging in with valid credentials
            login_page.verify_redirect_to_inventory()  # Verifying the redirection to inventory page

            # Task 2: Add items from Inventory Page
            inventory_page = InventoryPage(self.driver)
            inventory_page.sort_items_by_price(
                "low_to_high"
            )  # Sorting items by price from low to high
            inventory_page.add_item_to_cart(
                "Sauce Labs Backpack"
            )  # Adding item to cart
            inventory_page.add_item_to_cart(
                "Sauce Labs Bike Light"
            )  # Adding another item to cart
            assert inventory_page.get_cart_count() == 2, (
                "Cart count should be 2 after adding two items."
            )  # Validation of cart count

            # Task 3: Add item from Product Details Page
            inventory_page.navigate_to_product_details(
                "Sauce Labs Onesie"
            )  # Navigate to product details
            product_details_page = ProductDetailsPage(self.driver)
            product_details_page.add_to_cart()  # Adding item from details page to the cart
            assert product_details_page.get_cart_count() == 3, (
                "Cart count should be 3 after adding one more item."
            )  # Validate cart count

            # Task 4: Remove item from Cart
            self.driver.get(
                "https://www.saucedemo.com/cart.html"
            )  # Navigate to the cart page
            cart_page = CartPage(self.driver)
            cart_page.remove_item_by_price_range(
                8, 10
            )  # Removing an item priced between $8 and $10
            assert cart_page.get_cart_count() == 2, (
                "Cart count should be 2 after removing one item."
            )  # Validate cart count

            # Task 5: Checkout Workflow
            cart_page.click_checkout()  # Clicking on the checkout button
            checkout_page = CheckoutPage(self.driver)
            checkout_page.fill_checkout_form(
                "John", "Doe", "12345"
            )  # Filling out the checkout form
            checkout_page.complete_purchase()  # Completing the purchase
            checkout_page.verify_success_message()  # Verifying the success message after purchase

            # Task 6: Logout
            login_page.logout()  # Logging out after completing all tasks

        finally:
            self.teardown()  # Ensures WebDriver is properly closed after the test
