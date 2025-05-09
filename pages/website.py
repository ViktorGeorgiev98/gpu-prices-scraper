from pages.base import Base_Page
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Website(Base_Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.cookies_header_by = (By.ID, "cookiescript_header")
        self.close_cookies_button_by = (By.ID, "cookiescript_close")
        self.dashboard_search_field_by = (By.XPATH, "//form[@id='search']//input")

    def close_cookies_if_present(self) -> None:
        if self.element_displayed(*self.cookies_header_by):
            print("Cookies displayed, let us close them")
            self.sleep(1)
            self.click(*self.close_cookies_button_by)
            print("Closed cookies")
        else:
            print("No need to close cookies")

    def search_for_gpu(self, gpu_name: str) -> None:
        print("Write gpu name in dashboard search field")
        self.send_keys(
            *self.dashboard_search_field_by, gpu_name + Keys.RETURN
        )  # click enter
        self.wait_for_page_load()
        print(f"Searched for {gpu_name}")
