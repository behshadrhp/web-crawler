from selenium import webdriver
from selenium.webdriver.common.by import By


# get driver & site
driver = webdriver.Firefox()
driver.get("https://searx.thegpm.org/")

# get search textbox & send text
search_textbox = driver.find_element(by=By.ID, value="q")
search_textbox.send_keys("Hello World")

# get search buttonbox & click
search_buttonbox = driver.find_element(by=By.CLASS_NAME, value="hide_if_nojs")
search_buttonbox.click()

# exit from webdriver
driver.quit()
