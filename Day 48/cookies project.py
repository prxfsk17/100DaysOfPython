from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep, time

url="https://ozh.github.io/cookieclicker"
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver=webdriver.Chrome(options=chrome_options)
driver.get(url)
sleep(3)
driver.find_element(By.ID, value="langSelect-EN").click()
sleep(2)
cookie = driver.find_element(By.ID, value="bigCookie")

wait_time=5
timeout=time()+wait_time
game_time = time() + 60 * 1

while True:
    cookie.click()

    if time()-timeout>0:
        items_to_buy=driver.find_elements(By.CSS_SELECTOR, value=".product.unlocked.enabled")
        if len(items_to_buy)>0:
            item_to_buy=items_to_buy[-1]
            item_to_buy.click()
        timeout=time()+wait_time
    if time()-game_time>0:
        try:
            cookies_per_second = driver.find_element(By.ID, value="cookies").text.split("\n")[1]
            print(cookies_per_second)
        except NoSuchElementException:
            print("Couldn't get final cookie count")
        break