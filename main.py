from selenium import webdriver
from pages.navigator import Navigator
from pages.website import Website


url = "https://desktop.bg/"


driver = webdriver.Chrome()


try:
    navigator = Navigator(driver)
    website = navigator.go_to(url)
    (
        website.search_for_gpu("Nvidia rtx 5070 ti")
        .select_gpu_only_checkbox()
        .get_all_gpus_and_make_csv()
    )
except Exception as e:
    raise RuntimeError(f"Error: {e}")
finally:
    driver.quit()
