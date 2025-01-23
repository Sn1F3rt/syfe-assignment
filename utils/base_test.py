from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver


class BaseTest:
    """
    A base class for setting up and tearing down Selenium WebDriver tests.
    """

    def setup(self) -> None:
        """
        Sets up the WebDriver for the test.
        - Uses ChromeDriver via WebDriver Manager for automatic installation.
        - Maximizes the browser window.
        - Navigates to the SauceDemo homepage.
        """
        # noinspection PyAttributeOutsideInit
        self.driver: WebDriver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")

    def teardown(self) -> None:
        """
        Tears down the WebDriver instance by quitting the browser.
        - Ensures proper cleanup after each test run.
        """
        if self.driver:
            self.driver.quit()
