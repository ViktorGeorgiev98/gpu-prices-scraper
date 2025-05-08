from selenium import webdriver
from pages.navigator import Navigator
from pages.website import Website


url = "https://desktop.bg/"


driver = webdriver.Chrome()


try:
    navigator = Navigator(driver)
    website = navigator.go_to(url)
except Exception as e:
    raise RuntimeError(f"Navigation to {url} failed: {e}")
finally:
    driver.quit()
