from selenium import webdriver
from selenium.webdriver.common.by import By


# get website & webdriver
driver = webdriver.Firefox()
driver.get("https://yandex.com/")

# get search textbox & send word
search_textbox = driver.find_element(by=By.CLASS_NAME, value="search3__input")
search_textbox.send_keys("Hello World")

# get search buttonbox & click
search_buttonbox = driver.find_element(by=By.CLASS_NAME, value="search3__button")
search_buttonbox.click()

# close driver
driver.quit()
