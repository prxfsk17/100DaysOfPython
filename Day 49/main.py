from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as ec

def retry(func, retries=7, description=None):
    print(description)
    while retries > 0:
        print(f"Attempt:{8-retries}")
        if func() == True:
            return
        retries-=1

     # The password you used during registration
counters = {
    "booked" : 0,
    "waitlisted" : 0,
    "already" : 0,
    "total" : 0
}
GYM_URL = "https://appbrewery.github.io/gym/"
detailed_info="\n"
ACCOUNT_EMAIL = "prxfsktest@gmail.com"  # The email you registered with
ACCOUNT_PASSWORD = "qwerty123456"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(chrome_options)
driver.get(GYM_URL)
wait = WebDriverWait(driver, 2)

def create_driver():
    try:

        wait.until(ec.element_to_be_clickable((By.ID, "login-button"))).click()
        email=wait.until(ec.presence_of_element_located((By.ID, "email-input")))
        password=wait.until(ec.presence_of_element_located((By.ID, "password-input")))
        email.clear()
        email.send_keys(ACCOUNT_EMAIL)
        password.clear()
        password.send_keys(ACCOUNT_PASSWORD)
        driver.find_element(By.ID, value="submit-button").click()
        wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))
        return True
    except:
        return False

def booking():
    try:
        global detailed_info
        day_groups = driver.find_elements(By.CSS_SELECTOR, value='div[id^="day-group"]')
        for day in day_groups:
            day_title = day.find_element(By.TAG_NAME, "h2").text

            if "Mon" in day_title or "Thu" in day_title:
                time_texts = day.find_elements(By.CSS_SELECTOR, "p[id^='class-time-']")
                for time_text in time_texts:
                    if "6:00 PM" in time_text.text:
                        index = time_texts.index(time_text)
                        class_name = day.find_elements(By.CSS_SELECTOR, "h3[id^='class-name-']")[index].text
                        button = day.find_elements(By.CSS_SELECTOR, "button[id^='book-button-']")[index]
                        t = button.text
                        class_info = f"{class_name} on {day_title}"
                        if t == "Book Class":
                            print(f"✓ Booked: {class_info}")
                            button.click()
                            counters["booked"] += 1
                            counters["total"] += 1
                            detailed_info += f"Booked: {class_info}\n"
                        elif t == "Join Waitlist":
                            print(f"✓ Joined waitlist for: {class_info}")
                            button.click()
                            counters["waitlisted"] += 1
                            counters["total"] += 1
                            detailed_info += f"Joined waitlist for: {class_info}\n"
                        elif t == "Booked":
                            print(f"✓ Already booked: {class_info}")
                            counters["already"] += 1
                            counters["total"] += 1
                            detailed_info += f"Already booked: {class_info}\n"
                        elif t == "Waitlisted":
                            print(f"✓ Already on waitlist: {class_info}")
                            counters["already"] += 1
                            counters["total"] += 1
                            detailed_info += f"Already waitlisted: {class_info}\n"
        return True
    except:
        return False

def check_bookings():
    try:
        verifying = ""
        driver.find_element(By.ID, value="my-bookings-link").click()
        wait.until(ec.presence_of_element_located((By.ID, "my-bookings-link")))
        bookings = driver.find_elements(By.CSS_SELECTOR, value='h3[id^="booking-class-name-booking"]')
        waitlisting = driver.find_elements(By.CSS_SELECTOR, value='h3[id^="waitlist-class-name-waitlist"]')

        for booking in bookings:
            verifying += f"✓ Verified: {booking.text}\n"
        for waiting in waitlisting:
            verifying += f"✓ Verified: {waiting.text}\n"
        print("--- VERIFYING ON MY BOOKINGS PAGE ---\n")
        print(verifying)
        length = len(bookings) + len(waitlisting)
        if length == counters["total"]:
            print("✅ SUCCESS: All bookings verified!")
        else:
            print(f"❌ MISMATCH: Missing {counters["total"] - length} bookings")
        return True
    except:
        return False

retry(create_driver, 7, "Trying to login")
retry(booking, 7, "Booking classes")
print(f'''
--- BOOKING SUMMARY ---
Classes booked: {counters["booked"]}
Waitlists joined: {counters["waitlisted"]}
Already booked/waitlisted: {counters["already"]}
Total Tuesday & Thursday 6pm classes processed: {counters["total"]}
''')
retry(check_bookings, 7, "Verifying bookings")

# print(detailed_info)