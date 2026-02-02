import time

import numpy as np
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def click_element_with_retry(xpath, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            element = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            return True
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(1)

search_item = input("Поиск по каталогу онлайнер (Минск), что вы хотите сравнить?\n")

url="https://catalog.onliner.by/"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
search_bar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div/header/div[3]/div/div[2]/div[1]/div[1]/input'))
    )
search_bar.send_keys(search_item)

first_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[1]/div[2]/ul/li/a/div/div[2]/div/a"))
    )
first_item.click()
try:
    cookies = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit-button"))
        )
    cookies.click()
except NoSuchElementException as e:
    print("no cookies found")
name = driver.find_element(By.CLASS_NAME, 'catalog-masthead__title')
print('='*50)
print(name.text)
print('='*50)
print()
try:
    click_element_with_retry(
        '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[1]/div[2]/div[4]/div[4]/a')
except TimeoutException as e:
    print("No AI description found\n")
offers_form = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "offers-form"))
)
try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/div"))
    )
    description_of_AI = element.text
    close_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/span'))
    )
    close_button.click()
    print(description_of_AI)
except:
    print("="*50)
try:
    click_element_with_retry('//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/aside/div[last()]/a')
except TimeoutException as e:
    print(e.msg)
try:
    offers = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[2]/div[1]/div/div[3]/div/div[3]'))
    )
    try:
        click_element_with_retry('//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[2]/div[1]/div/div[3]/div/div[3]/div[6]/span')
    except:
        print("There are not so many offers...")
    offer_elements = offers.find_elements(By.CSS_SELECTOR,
    'div[class*="offers-list__description"][class*="offers-list__description_alter-other"][class*="offers-list__description_huge-alter"]'
                                          )
    offer_texts = [float(elem.text.strip().replace(',','.')[:-3]) for elem in offer_elements if elem.text.strip()]
    if len(offer_texts) == 0:
        offer_texts.append(float(driver.find_element(By.XPATH,
                                                '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[2]/div[1]/div/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div').text.strip().replace(',','.')[:-3])
                           )
    offers_np = np.array(offer_texts)

    print("\nDescription of price:")
    print(f"Min price: {offers_np.min():.2f}")
    print(f"Mean price: {offers_np.mean():.2f}")
    print(f"Max price: {offers_np.max():.2f}")

except TimeoutException as e:
    print(e.msg)
