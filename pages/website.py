from pages.base import Base_Page
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv


class Website(Base_Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.cookies_header_by = (By.ID, "cookiescript_header")
        self.close_cookies_button_by = (By.ID, "cookiescript_close")
        self.dashboard_search_field_by = (By.XPATH, "//form[@id='search']//input")
        self.gpu_only_checkbox_by = (By.ID, "type_in_desktop_video_card")
        self.gpu_only_label_by = (
            By.XPATH,
            "//label[@for='type_in_desktop_video_card']",
        )
        self.spinner_by = (By.XPATH, "//i[@class='loading-icon']")
        self.all_gpus_found_by = (By.XPATH, "//ul[@class='products']//article")
        self.no_results_by = (
            By.XPATH,
            "//div[@class='message error']//*[contains(text(),'Няма резултат')]",
        )

    def close_cookies_if_present(self) -> None:
        self.wait_for_page_load()
        if self.element_displayed(*self.cookies_header_by):
            print("Cookies displayed, let us close them")
            self.sleep(1)
            self.click(*self.close_cookies_button_by)
            print("Closed cookies")
        else:
            print("No need to close cookies")
        return self

    def search_for_gpu(self, gpu_name: str) -> None:
        self.wait_for_page_load()
        print("Write gpu name in dashboard search field")
        self.send_keys(
            *self.dashboard_search_field_by, gpu_name + Keys.RETURN
        )  # click enter
        self.wait_for_page_load()
        if self.element_displayed(*self.no_results_by):
            raise Exception(f"No results found for the search param: {gpu_name}")
        print(f"Searched for {gpu_name}")
        return self

    def select_gpu_only_checkbox(self) -> None:
        self.wait_for_page_load()
        print("We need to select only gpu option from filters")
        if self.find_element(*self.gpu_only_checkbox_by).is_selected():
            print("Checkbox for gpu only is already selected")
        else:
            print("Enable gpu only checkbox")
            self.click(*self.gpu_only_label_by)
            self.wait_for_spinner(tries=10)
            self.wait_for_page_load()
        return self

    def wait_for_spinner(self, tries: int) -> None:
        self.wait_for_page_load()
        print("Check for spinner")
        for _ in range(tries):
            try:
                if self.find_element(*self.spinner_by).is_displayed():
                    print("Spinner present, wait")
                    self.sleep(1)
                else:
                    print("Spinner not visible")
                    return
            except Exception as e:
                print("Spinner xpath might be wrong, or spinner is not displayed")

    def get_all_gpus_and_make_csv(self):
        self.wait_for_page_load()
        self.wait_for_spinner(tries=10)
        gpu_cards = self.find_elements(*self.all_gpus_found_by)
        if len(gpu_cards) == 0:
            raise Exception("GPU list is empty, check")
        gpus = []
        for card in gpu_cards:
            try:
                gpu_name = card.find_element(By.XPATH, "//h2[@itemprop='name']").text
                gpu_price = card.find_element(
                    By.XPATH, "//div[@class='price-container']//span[@itemprop='price']"
                ).text
                gpus.append({"Name": gpu_name, "Price": gpu_price})
            except Exception as e:
                print(f"Skipping card due to error: {e}")

        try:
            with open("gpus.csv", newline="", mode="w", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Name", "Price"])
                writer.writeheader()
                writer.writerows(gpus)
            print("CSV file with gpus created")
        except Exception as e:
            print(f"Exception: {e}")
        return self
