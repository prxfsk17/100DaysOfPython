from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from dotenv import load_dotenv

load_dotenv()
PROMISED_DOWN=40
PROMISED_UP=8
EMAIL=os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")
SPEEDTEST_URL="https://www.speedtest.net/ru"
TWITTER_URL="https://x.com"

class InternetSpeedTwitterBot:

    def __init__(self):
        self.down=0
        self.up=0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        prefs = {"autofill.profile_enabled": False}
        chrome_options.add_experimental_option("prefs", prefs)
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        self.driver = webdriver.Chrome(chrome_options)
        self.wait=WebDriverWait(self.driver, 60)
        self.main_window_handle = None
        self.new_window_handle = None

    def get_internet_speed(self, url):
        self.driver.get(url)
        self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "js-start-test.test-mode-multi")))
        start_button=self.driver.find_element(By.CLASS_NAME, value='js-start-test.test-mode-multi')
        start_button.click()
        self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-server-select")))
        self.down = self.driver.find_element(By.CLASS_NAME, value='result-data-large.number.result-data-value.download-speed').text
        self.up = self.driver.find_element(By.CLASS_NAME, value='result-data-large.number.result-data-value.upload-speed').text

    def tweet_at_provider(self, url):
        self.driver.get(url)


        self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a')))
        login_button = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a')
        login_button.click()

        self.main_window_handle=self.driver.current_window_handle

        self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[1]')))
        apple_button = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[1]')
        apple_button.click()

        self.switch_to_new_window()

        #email
        self.wait.until(ec.presence_of_element_located((By.ID, 'account_name_text_field')))
        input_email = self.driver.find_element(By.ID, value='account_name_text_field')
        input_email.send_keys(EMAIL)
        next_button = self.driver.find_element(By.ID, value='sign-in')
        next_button.click()

        # #password - entered by user
        # self.wait.until(ec.presence_of_element_located((By.ID, 'password_text_field')))
        # input_email = self.driver.find_element(By.ID, value='password_text_field')
        # self.driver.execute_script("arguments[0].setAttribute('autocomplete', 'new-password')", input_email)
        # input_email.send_keys(PASSWORD)
        # next_button = self.driver.find_element(By.CLASS_NAME, value='signin-v2__buttons-wrapper__button-wrapper__button__text')
        # next_button.click()

        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'button.button-primary.last.nav-action.pull-right.weight-medium')))
        finish_button = self.driver.find_element(By.CLASS_NAME, value='button.button-primary.last.nav-action.pull-right.weight-medium')
        finish_button.click()

        self.switch_to_main_page()

        self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')))
        input_tweet = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
        input_tweet.send_keys(f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?")
        next_button = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')
        next_button.click()

    def switch_to_new_window(self):
        for handle in self.driver.window_handles:
            if handle != self.main_window_handle:
                self.new_window_handle = handle
                break
        self.driver.switch_to.window(self.new_window_handle)


    def switch_to_main_page(self):
        self.driver.switch_to.window(self.main_window_handle)

driver_speed = InternetSpeedTwitterBot()
driver_speed.get_internet_speed(SPEEDTEST_URL)
driver_speed.tweet_at_provider(TWITTER_URL)
