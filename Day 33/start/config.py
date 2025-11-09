import smtplib
def send_notification():
    my_gmail = "alesspy7@gmail.com"
    my_pass = "ihxqntmwikiipsou"
    my_yahoo = "alesspy7@yahoo.com"

    #host: gmail - smtp.gmail.com, yahoo - smtp.mail.yahoo.com, hotmail - smtp.live.com
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=my_pass)
        connection.sendmail(from_addr=my_gmail,
                            to_addrs=my_yahoo,
                            msg=f"Subject:ISS\n\nISS is near to you, look up!")