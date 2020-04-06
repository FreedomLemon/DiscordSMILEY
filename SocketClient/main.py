import websockets, asyncio, json, threading

from colorama import Fore, init
init(convert=True)

token = ''

class Client:
    def __init__(self, token: str):
        self.token = token
        self.heartbeat = None
        self.socket = None
        self.sessionID = None
        self.seq = None
    
    async def resume(self):
        if self.socket == None:
            return

        if self.socket.close_code == 1001:
            await self.send(json.dumps({
                "token": token,
                "session_id": self.sessionID,
                "seq": self.seq
            }))

    async def connect(self):
        self.socket = await websockets.connect("wss://gateway.discord.gg/?encoding=json&v=6")
        self.heartbeat = json.loads((await self.socket.recv()))['d']['heartbeat_interval']

    async def identify(self):
        if self.socket == None:
            await self.connect()

        await self.socket.send(json.dumps({
            "op":2,
            "d": {  
                "token": token,
                "properties":{
                    "os":"MomOS",
                    "browser":"Pixels",
                    "device":"",
                    "browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                    "os_version":"xp"
                    }
                }}))

        self.sessionID = json.loads(await self.socket.recv())['d']['session_id']

    async def send(self, _data: json.dumps):
        if self.socket == None:
            await self.identify()
        
        await self.socket.send(_data)

        print(Fore.GREEN + await self.socket.recv() + "\n")

    async def messages(self):
        if self.socket == None:
            await self.identify()

        while True:
            _data = (await self.socket.recv())
            self.seq = json.loads(_data)['s']
            print( Fore.CYAN + _data + "\n")

asyncio.run(Client(token).messages())
