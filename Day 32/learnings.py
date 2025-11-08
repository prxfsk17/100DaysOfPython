import datetime as dt
now = dt.datetime.now()
if now.weekday()==5:
    import random
    with open("Day 32/quotes.txt") as f:
        quotes = f.readlines()
    quote = random.choice(quotes)
    author = quote.split('"')[-1][3:-1]
    quote = quote.split('"')[1]

    import smtplib
    my_gmail = "alesspy7@gmail.com"
    my_pass = "ihxqntmwikiipsou"
    my_yahoo = "alesspy7@yahoo.com"

    #host: gmail - smtp.gmail.com, yahoo - smtp.mail.yahoo.com, hotmail - smtp.live.com
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=my_pass)
        connection.sendmail(from_addr=my_gmail,
                            to_addrs=my_yahoo,
                            msg=f"Subject:{author} tells you:\n\n{quote}")


