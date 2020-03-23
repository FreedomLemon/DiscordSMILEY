import requests, time, sys

from colorama import Fore, init
init(convert=True)


print(f"[{Fore.CYAN} Webhook Url {Fore.RESET}]")
webhook = str(input(" > "))
print(f"[{Fore.CYAN} Message {Fore.RESET}]")
message = str(input(" > "))
print(f"[{Fore.CYAN} Delay {Fore.RESET}({Fore.CYAN}seconds{Fore.RESET})]")
delay = int(input(" > "))
print('\n')

while True:
    try:
        time.sleep(delay)
        _data = requests.post(webhook, json={'content': message})

        if _data.status_code == 204:
            print(f"[{Fore.CYAN} Sent a new message {Fore.RESET}]")
    except KeyboardInterrupt:
        sys.exit(0)
