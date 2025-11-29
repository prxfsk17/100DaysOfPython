import os
from time import sleep
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Filler:

    def __init__(self):
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver=webdriver.Chrome(chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = os.getenv("URL_FORMS")

    def send_record_to_sheet(self, record):
        print(record)

        self.driver.get(self.url)
        self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        address_input=self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_input=self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_input=self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_input.send_keys(record["address"])
        price_input.send_keys(record["price"])
        link_input.send_keys(record["link"])
        submit_button=self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit_button.click()
        sleep(1.1)