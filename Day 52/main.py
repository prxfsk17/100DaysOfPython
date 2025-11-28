import os

from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Keys

load_dotenv()
EMAIL=os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")
SIMILAR=os.getenv("similar_account")

class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        self.driver = webdriver.Chrome(chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def login(self):
        self.wait.until(ec.presence_of_element_located((By.ID, 'loginForm')))
        login_input = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
        password_input = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
        login_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)
        enter_button=self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div[1]/div[3]/button')
        enter_button.click()

    def find_followers(self):
        # self.wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="mount_0_0_FB"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[4]/span/div/a')))
        # search_button=self.driver.find_element(By.XPATH, value='//*[@id="mount_0_0_Hk"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[4]/span/div/a')
        # search_button.click()
        # search_input=self.driver.find_element(By.XPATH, value='//*[@id="mount_0_0_Hk"]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/input')
        # search_input.send_keys()
        # account=self.driver.find_element(By.XPATH, value='//*[@id="mount_0_0_Hk"]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/a')
        # account.click()
        # sleep(15)
        self.driver.get(f"https://instagram.com/{SIMILAR}/followers")
        sleep(5)
        # self.wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="mount_0_0_Hk"]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/section/main/div/div/header/div/section[2]/div[1]/div[3]/div[2]/a')))
        # followers_button=self.driver.find_element(By.XPATH, value='//*[@id="mount_0_0_Hk"]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/section/main/div/div/header/div/section[2]/div[1]/div[3]/div[2]/a')
        # followers_button.click()
        followers_button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '/{SIMILAR}/followers/')]"))
        )
        followers_button.click()


    def follow(self):
        sleep(3)
        buttons = self.driver.find_elements(By.XPATH, value="//button[contains(text(), 'Подписаться')]")
        if len(buttons) == 0:
            for i in range(1, 49):
                buttons.append(self.driver.find_element(By.XPATH, f'/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[{i}]/div/div/div/div[3]/div/button'))
        for but in buttons:
            try:
                sleep(1)
                but.click()
            except ElementClickInterceptedException:
                sleep(1)
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Отмена')]")
                cancel_button.click()

instaFollower = InstaFollower()
instaFollower.driver.get("https://instagram.com")
# instaFollower.login()
instaFollower.find_followers()
instaFollower.follow()