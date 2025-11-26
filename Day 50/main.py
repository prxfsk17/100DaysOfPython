from time import sleep

from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os

TINDER_URL = "https://tinder.com/"
ACCOUNT_EMAIL = "alesspy7@gmail.com"
# ACCOUNT_PASSWORD = "qwerty123456"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(chrome_options)
driver.get(TINDER_URL)
wait = WebDriverWait(driver, 2)

#logging
wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="u1559600490"]/div/div[1]/div/main/div[1]/div/div/div/div/div[1]/header/div/div[2]/div[2]/a/div[2]/div[2]/div'))).click()
sleep(5)
google_login=driver.find_element(By.XPATH, value='//*[@id="gsi_778363_137902"]')
driver.get(google_login.get_attribute("href"))
driver.get("https://accounts.google.com/gsi/button?type=standard&logo_alignment=left&shape=pill&size=large&theme=filled_blue&text=continue_with&width=352&click_listener=()%3D%3E%7Bu(%7Buuid%3Ah.kQP%2Ctype%3Ap.cU%7D)%7D&is_fedcm_supported=true&client_id=230402993429-g4nobau40t3v3j0tvqto4j8f35kil4hf.apps.googleusercontent.com&iframe_id=gsi_693562_619691&cas=3%2FOky6W5Jfv61rNJpuVg0bwCMHfc46R1geOhJbqZWBM")

#Switch to Facebook login window
sleep(2)
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title)

#Login and hit enter
email = driver.find_element(By.XPATH, value='//*[@id="email"]')
password = driver.find_element(By.XPATH, value='//*[@id="pass"]')
email.send_keys(ACCOUNT_EMAIL)
password.send_keys(ACCOUNT_EMAIL)
password.send_keys(Keys.ENTER)

#Switch back to Tinder window
driver.switch_to.window(base_window)
print(driver.title)

#Allow location
allow_location_button = driver.find_element(By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
allow_location_button.click()

#Disallow notifications
notifications_button = driver.find_element(By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
notifications_button.click()

#Allow cookies
cookies = driver.find_element(By.XPATH, value='//*[@id="content"]/div/div[2]/div/div/div[1]/button')
cookies.click()

for n in range(100):

    #Add a 1 second delay between likes.
    sleep(1)

    try:
        print("called")
        like_button = driver.find_element(By.XPATH, value=
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_button.click()

    #Catches the cases where there is a "Matched" pop-up in front of the "Like" button:
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, value=".itsAMatch a")
            match_popup.click()

        #Catches the cases where the "Like" button has not yet loaded, so wait 2 seconds before retrying.
        except NoSuchElementException:
            sleep(2)

driver.quit()