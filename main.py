from time import sleep
from downloader import download_song
from uploader import upload_files
from mailer import send_mail
from form_getter import get_form_responses
from form_reloader import reload_form


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
            links = upload_files(download)
            print("Upload successfull")
            send_mail(name, links[0], email)
            print("Mail successfull")

            with open("./sent_mails.txt", "a") as f:
                f.write(uid)
                lines.add(uid)

            return True
    else:
        print("Skipped because already sent")

    return False


if __name__ == "__main__":
    while True:
        reload_form()
        sleep(10)
        for donna_url, name, email in get_form_responses():
            print(f"Handling {name}'s request to send {donna_url} to {email}...")

            if handle_request(donna_url, name, email):
                print(
                    f"{name}'s request to send {donna_url} to {email} was successfull"
                )
        print("\nWaiting two minutes and then trying again...")
        sleep(120)
