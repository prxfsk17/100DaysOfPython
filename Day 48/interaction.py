from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# url = "https://en.wikipedia.org/wiki/Main_Page"
url = "https://secure-retreat-92358.herokuapp.com"
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver=webdriver.Chrome(options=chrome_options)
driver.get(url)
# count=driver.find_element(By.ID, value="articlecount").find_elements(By.TAG_NAME, value="a")[1]
# print(count.text)
# # count.click()
# portals=driver.find_element(By.LINK_TEXT, value="Content portals")
# portals.click()
# search.send_keys("Python")
# search.send_keys(Keys.ENTER)

fname=driver.find_element(By.NAME, value="fName")
lname=driver.find_element(By.NAME, value="lName")
email=driver.find_element(By.NAME, value="email")
but=driver.find_element(By.TAG_NAME, value="button")
fname.send_keys("myself")
lname.send_keys("my surname")
email.send_keys("email@of.mine")
but.click()