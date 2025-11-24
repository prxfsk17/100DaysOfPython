from selenium import webdriver
from selenium.webdriver.common.by import By

# url="https://www.amazon.de/dp/B0F22QYD7V/ref=sspa_dk_detail_6?pd_rd_i=B0F24TXQY8&pd_rd_w=2vT0s&content-id=amzn1.sym.99a46b10-6bb0-41eb-aa22-b26ae1e31690&pf_rd_p=99a46b10-6bb0-41eb-aa22-b26ae1e31690&pf_rd_r=HEZHSMF2S6HF82WNX94T&pd_rd_wg=TsVZr&pd_rd_r=6b4970a3-779e-4dbd-9cc4-29890165ccde&aref=hMfUQmsnqA&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM&th=1"
url="https://python.org/"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
# driver.find_element(By.CLASS_NAME, value="a-button-text").click()
# price_dollar=driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_cents=driver.find_element(By.CLASS_NAME, value="a-price-fraction")
# print(f"The price is {price_dollar.text}.{price_cents.text}")

# smth = driver.find_element(By.ID, value="some_id")

# search_bar = driver.find_element(By.NAME, value="q")
# print(search_bar.get_attribute("placeholder"))

# doc_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(doc_link.text)
# x_path='//*[@id="content"]/div/section/div[2]/div[1]/div/ul/li[2]/a'
# x_path_el = driver.find_element(By.XPATH, value=x_path)
# print(x_path_el.text)

menu = driver.find_element(By.XPATH, '//*[@id="content"]/div/section/div[2]/div[2]/div/ul')
list_of_dates = menu.find_elements(By.CSS_SELECTOR, value="li")
res = {}
for i in range(len(list_of_dates)):
    elem = {
        "time" : list_of_dates[i].find_element(By.CSS_SELECTOR, value="time").text,
        "name" : list_of_dates[i].find_element(By.CSS_SELECTOR, value="a").text
    }
    res[i]=elem
print(res)

# driver.close() # for tab
driver.quit() # for browser


