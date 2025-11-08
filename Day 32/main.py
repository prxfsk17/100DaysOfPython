##################### Extra Hard Starting Project ######################
# 2. Check if today matches a birthday in the birthdays.csv
import pandas
import datetime as dt
records = pandas.read_csv("birthdays.csv")
today = (dt.datetime.now().month, dt.datetime.now().day)
list_send_to=[{"name":row["name"],"email":row["email"]} for (index,row) in records.iterrows() if row["month"] == today[0] and row["day"]==today[1]]
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
if len(list_send_to)>0:
    my_gmail = "alesspy7@gmail.com"
    my_pass = "ihxqntmwikiipsou"
    import smtplib
    import random
    for person in list_send_to:
        letters=["letter_1.txt", "letter_2.txt", "letter_3.txt"]
        letter_path = random.choice(letters)
        with open(f"letters/{letter_path}") as f:
            letter = f.readlines()
        letter[0] = letter[0].replace("[NAME]", person["name"])
        letter = "".join(letter)
# 4. Send the letter generated in step 3 to that person's email address.
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_gmail, password=my_pass)
            connection.sendmail(from_addr=my_gmail,
                                to_addrs=person["email"],
                                msg=f"Subject:Happy Birthday!\n\n{letter}")



