from datetime import datetime
from os import system
import requests
import json

url = input("Please paste the URL of the meeting you want to download: ")
meeting_id = url.split("/")[-1].split("?")[0]
print("\rFound meeting ID: ", meeting_id)

auth_token = input("Auth token: ")

data = requests.get(
    f"https://gw.tldv.io/v1/meetings/{meeting_id}/watch-page?noTranscript=true",
    headers={"Authorization": auth_token},
)

try:
    response = json.loads(data.text)
    meeting = response.get("meeting", {})
    name = meeting.get("name", "No name")
    createdAt = meeting.get("createdAt", datetime.now())
    source = response.get("video", {}).get("source", None)
    date = datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%S.%fZ")
    normalised_date = date.strftime("%Y-%m-%d-%H-%M-%S")
    # Sanitize name for filename
    safe_name = name.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "-").replace("?", "-").replace("\"", "-").replace("<", "-").replace(">", "-").replace("|", "-")
    filename = f"{normalised_date}_{safe_name}"

    command = f'N_m3u8DL-RE "{source}" --save-dir "." --save-name "{filename}" --thread-count 16 --del-after-done'
    print(command)
    print("Downloading video...")
    system(command)

    with open(f"{filename}.json", "w") as f:
        f.write(data.text)

except Exception as e:
    print("Error encountered")
    print("Exception:", str(e))
    print("Raw response:")
    print(data.text)
