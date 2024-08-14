from selenium import webdriver
from selenium.webdriver.common.by import By


# get site & web driver
driver = webdriver.Firefox()
driver.get("https://www.bing.com/")

# get search textbox & send word
search_textbox = driver.find_element(by=By.ID, value="sb_form_q")
search_textbox.send_keys("Hello World")

# get search btn box & click
search_buttonbox = driver.find_element(by=By.ID, value="search_icon")
search_buttonbox.click()

# close driver
driver.quit()
