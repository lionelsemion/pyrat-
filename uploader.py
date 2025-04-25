import owncloud
import os
from dotenv import load_dotenv

load_dotenv()


oc = owncloud.Client("http://cloud.piratenpartei.ch/")
oc.login(os.getenv("NEXTCLOUD_USERNAME"), os.getenv("NEXTCLOUD_PASSWORD"))


def upload_files(files):
    links = []

    for file in files:
        links.append(upload_file(file))

    return links


def upload_file(file):
    path = f"Bern/2025 BEA/{file}"

    oc.put_file(path, f"./{file}")

    link_info = oc.share_file_with_link(path)

    return link_info.get_link()
