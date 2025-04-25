import requests
from bs4 import BeautifulSoup
import os


def download_song(donna_url: str, name: str, email: str):
    try:
        response = requests.get(donna_url)
    except:
        print(f"Failed to download.")
        return False

    if not response.ok:
        print(f"Failed to download. Status code: {response.status_code}")
        return False

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    # Get the div that wraps song info by ID
    song_div = soup.find("div", {"id": "songDiv"})

    # Inside this div, get the class that wraps the details
    details_div = song_div.find("div", class_="song-details-div")

    # Song name is in <h1> inside this class
    song_name = details_div.find("h1").get_text(strip=True)

    # Prompt is in the <p> tag inside the same class
    prompt = details_div.find("p").get_text(strip=True)

    # Extract the audio download URL from the <audio> tag
    audio_url = soup.find("audio")["src"]

    file_name = audio_url.split("/")[-1]

    response = requests.get(audio_url)

    if response.status_code == 200:
        if not os.path.exists("./songs"):
            os.makedirs("songs")

        with open("./songs/" + file_name, "wb") as f:
            f.write(response.content)
        print(f"Downloaded successfully as '{file_name}'")
        with open("./songs/" + file_name[:-3] + "txt", "w") as f:
            f.write(
                f'"{song_name}"\nBy {name} - {email}\n\nGenerated with musicdonna.com using the following prompt: \n\n{prompt}'
            )
        return ("songs/" + file_name, "songs/" + file_name[:-3] + "txt"), song_name
    else:
        print(f"Failed to download. Status code: {response.status_code}")
        return False
