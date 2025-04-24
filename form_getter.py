import requests
import csv

import os
from dotenv import load_dotenv

load_dotenv()


def get_form_responses():
    response = requests.get(os.getenv("CSV_URL"))

    with open("./responses.csv", "w") as f:
        f.write(response.text)

    with open("./responses.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        result = [
            (row["Link"], row["Name/Pseudonym"], row["Email-Adresse"]) for row in reader
        ]

    return result
