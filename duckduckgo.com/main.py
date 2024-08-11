from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get("https://duckduckgo.com")

# get input
search_box_input = driver.find_element(by=By.ID, value="searchbox_input")
search_box_input.send_keys("Hello world")

search_box_btn = driver.find_element(by=By.CLASS_NAME, value="searchbox_searchButton__F5Bwq")
search_box_btn.click()

driver.close()
