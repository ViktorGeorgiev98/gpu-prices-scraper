from pages.base import Base_Page
from pages.website import Website
from selenium.webdriver.common.by import By


class Navigator(Base_Page):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.driver = driver
        self.logo_by = (By.XPATH, "//a[@id='logo']")

    def go_to(self, url):
        self.driver.get(url)
        if self.element_displayed(locator=self.logo_by, tries=10):
            print("Website is opened")
        else:
            raise Exception("Website could not be reached")
        return Website
