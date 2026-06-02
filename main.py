##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import smtplib

my_email = "romariorodriguez67@gmail.com"
password = "xkqxnereoruddylz"

import datetime as dt
import pandas as pd
import random
from pathlib import Path

# __file__ means "this exact Python script".
# .parent means "the folder this script is sitting in".
SCRIPT_DIR = Path(__file__).parent
LETTER_TEMPLATE_1 = SCRIPT_DIR / "letter_templates" / "letter_1.txt"
LETTER_TEMPLATE_2 = SCRIPT_DIR / "letter_templates" / "letter_2.txt"
LETTER_TEMPLATE_3 = SCRIPT_DIR / "letter_templates" / "letter_3.txt"
BIRTHDAYS = SCRIPT_DIR / "birthdays.csv"
LETTER_TEMPLATE_GROUP = [LETTER_TEMPLATE_1, LETTER_TEMPLATE_2, LETTER_TEMPLATE_3]

# Pandas handles opening, parsing, and naming columns all at once
df = pd.read_csv(BIRTHDAYS)

now = dt.datetime.now()
year, month, day = now.year, now.month, now.day
# This creates a mask where both conditions are true
# 1. Create the filtered DataFrame
matching_rows = df[(df["month"] == month) & (df["day"] == day)]

# 2. Check if it actually found anything
if not matching_rows.empty:
    # Pull the 'name' column ONLY from the matching rows
    birthday_names = matching_rows["name"]
    birthday_emails = matching_rows["email"]
    with open(random.choice(LETTER_TEMPLATE_GROUP), "r") as file:
        template_content = file.read()  #

        # 2. Loop through each name and generate a personalized letter
        for name, email in zip(birthday_names, birthday_emails):
            # .replace() swaps [NAME] for the actual person's name
            personalized_letter = template_content.replace("[NAME]", name)
            print(personalized_letter)

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=email,
                                    msg=f"Subject:Happy Birthday\n\n{personalized_letter}\n\n")
            print("Email sent successfully!")
else:
    pass

