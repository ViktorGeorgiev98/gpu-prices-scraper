from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Base_Page:
    def __init__(self, driver):
        self.driver = driver
        self.wait_time = 10  # save timeout as number
        self.wait = WebDriverWait(driver, self.wait_time)  # reuse this if you want

    def sleep(self, seconds: int) -> None:
        time.sleep(seconds)

    def click(self, locator: tuple) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def get_text(self, locator: tuple) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def send_keys(self, locator: tuple, text: str) -> None:
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)

    def element_displayed(self, locator: tuple, tries: int = 5) -> bool:
        for _ in range(tries):
            try:
                if self.driver.find_element(*locator).is_displayed():
                    print("Element displayed: True")
                    return True
            except:
                pass
            self.sleep(1)
        print("Element displayed: False")
        return False

    def wait_for_page_load(self):
        WebDriverWait(self.driver, self.wait_time).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
