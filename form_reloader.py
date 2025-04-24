import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def reload_form():
    USERNAME = os.getenv("NEXTCLOUD_USERNAME")
    PASSWORD = os.getenv("NEXTCLOUD_PASSWORD")

    login_url = "https://cloud.piratenpartei.ch/login"
    session = requests.Session()

    # 1. Get login page to fetch CSRF token and set cookies
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, "html.parser")
    request_token = soup.head.get("data-requesttoken")

    if not request_token:
        raise Exception("Login token not found!")

    # 2. Prepare form data for login POST
    login_data = {
        "user": USERNAME,
        "password": PASSWORD,
        "timezone": "Europe/Berlin",
        "timezone_offset": "120",  # adjust depending on your timezone
        "requesttoken": request_token,
    }

    # 3. Submit login form
    response = session.post(login_url, data=login_data)

    # Optional: verify login success
    if USERNAME not in response.text:
        print("Login failed — check credentials or token logic.")
        print(f"Status: {response.status_code}")
        exit()

    print("Login successful.")

    # 4. Use requesttoken again (from POST-login HTML)
    soup = BeautifulSoup(response.text, "html.parser")
    api_token = soup.head.get("data-requesttoken")

    # 5. API Call
    export_url = "https://cloud.piratenpartei.ch/ocs/v2.php/apps/forms/api/v3/forms/12/submissions/export"
    headers = {
        "requesttoken": api_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
    }
    payload = {
        "path": "/Bern/2025 BEA/songs/AI Song Contest (responses).csv",
        "fileFormat": "csv",
    }

    export_response = session.post(export_url, headers=headers, json=payload)

    if export_response.ok:
        print("Export successful!")
    else:
        print(f"Export failed. Status: {export_response.status_code}")
        print(export_response.text)
