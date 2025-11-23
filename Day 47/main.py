from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
# URL_FIFA="https://www.amazon.de/dp/B0FGLW6TF5?ref=dlx_black_dg_dcl_B0FGLW6TF5_dt_sl7_60_pi&pf_rd_r=Q0GN8M62N495G43NCVFD&pf_rd_p=bcadc3bb-cdd2-4bbc-a284-57981073c560&th=1"
URL_F1="https://www.amazon.de/dp/B0F22QYD7V/ref=sspa_dk_detail_6?pd_rd_i=B0F24TXQY8&pd_rd_w=2vT0s&content-id=amzn1.sym.99a46b10-6bb0-41eb-aa22-b26ae1e31690&pf_rd_p=99a46b10-6bb0-41eb-aa22-b26ae1e31690&pf_rd_r=HEZHSMF2S6HF82WNX94T&pd_rd_wg=TsVZr&pd_rd_r=6b4970a3-779e-4dbd-9cc4-29890165ccde&aref=hMfUQmsnqA&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM&th=1"
HEADERS={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,pl;q=0.6",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"99\", \"Opera GX\";v=\"123\", \"Chromium\";v=\"139\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0",
    "X-Amzn-Trace-Id": "Root=1-6922ca0f-73396a857071a8bf739fe5f1"
}

response = requests.get(URL_F1, headers=HEADERS)
response.raise_for_status()

SENDER=os.getenv("SMTP_SENDER")
PASSWORD=os.getenv("SMTP_PASSWORD")
RECIPIENT=os.getenv("SMTP_REC")
TARGET_PRICE=30

soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())
price_whole=soup.find(class_="a-price-whole").getText()
price_fract=soup.find(class_="a-price-fraction").getText()
product=soup.find(id="productTitle").getText().strip()
price=float(f"{price_whole}{price_fract}")
if price<TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as conn:
        conn.starttls()
        conn.login(user=SENDER, password=PASSWORD)
        conn.sendmail(from_addr=SENDER, to_addrs=RECIPIENT,
                      msg=f"Subject:Amazon Price Alert!\n\n"
                          f"{product} is now ${price}.\nYou can buy there: {URL_F1}".encode("utf-8"))