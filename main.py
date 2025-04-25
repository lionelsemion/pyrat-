from time import sleep
from downloader import download_song
from uploader import upload_file, upload_files
from mailer import send_mail
from form_getter import get_form_responses
from form_reloader import reload_form
import csv


try:
    with open("./contestants.csv", "r") as f:
        pass
except FileNotFoundError:
    fields = ["name", "email", "song_name", "song_file", "share_link"]
    with open(r"./contestants.csv", "x") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

try:
    with open("./sent_mails.txt", "r") as f:
        lines = set(f.readlines())
except FileNotFoundError:
    lines = set()


def handle_request(donna_url: str, name: str, email: str):
    uid = f"{f"{donna_url} by {name} sent to {email}"}\n"

    if uid not in lines:  # skip if mail already sent
        download = download_song(donna_url, name, email)
        if download:
            links = upload_files(download[0])
            print("Upload successfull")
            send_mail(name, links[0], email)
            print("Mail successfull")

            with open("./sent_mails.txt", "a") as f:
                f.write(uid)
                lines.add(uid)

            fields = [name, email, download[1], download[0][0], links[0]]
            with open(r"./contestants.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow(fields)

            return True
    else:
        print("Skipped because already sent")

    return False


if __name__ == "__main__":
    while True:
        reload_form()
        sleep(10)

        updated = False

        for donna_url, name, email in get_form_responses():
            print(f"Handling {name}'s request to send {donna_url} to {email}...")

            if handle_request(donna_url, name, email):
                updated = True
                print(
                    f"{name}'s request to send {donna_url} to {email} was successfull"
                )

        if updated:
            print("Uploading contestants.csv...")
            upload_file("contestants.csv")
            print("Upload successfull")

        print("\nWaiting two minutes and then trying again...")
        sleep(120)
