import time
import requests
from datetime import datetime, timedelta
import re

def read_data():
    with open('data.txt', 'r') as file:
        lines = file.read().splitlines()

    accounts = []
    account = {}
    for line in lines:
        if line.startswith('account[address]:'):
            if account:
                accounts.append(account)
            account = {'initDataUnsafe': {}}
        if 'account[address]:' in line:
            account['address'] = lines[lines.index(line) + 1]
        if 'account[walletStateInit]:' in line:
            account['walletStateInit'] = lines[lines.index(line) + 1]
        if 'account[publicKey]:' in line:
            account['publicKey'] = lines[lines.index(line) + 1]
        if 'initData:' in line:
            init_data = lines[lines.index(line) + 1]
            account['initData'] = init_data
            params = init_data.split('&')
            for param in params:
                key, value = param.split('=')
                key_parts = key.split('[')
                if len(key_parts) == 1:
                    account[key] = value
                else:
                    sub_key = key_parts[1][:-1]
                    account['initDataUnsafe'][sub_key] = value

    if account:
        accounts.append(account)

    return accounts

def extract_username(init_data):
    match = re.search(r'username%22%3A%22([^%]+)%22', init_data)
    return match.group(1) if match else "Unknown"

def countdown(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"\rCountdown: {remaining_time}", end='')
        time.sleep(1)
    print()

def process_accounts():
    accounts = read_data()
    total_accounts = len(accounts)
    print(f"Total accounts: {total_accounts}")

    previous_username = None

    for index, account in enumerate(accounts):
        username = extract_username(account['initData'])

        if username == previous_username:
            print(f"\nDetected duplicate username: {username}. Reloading data.")
            accounts = read_data()
            account = accounts[index]
            username = extract_username(account['initData'])

        print(f"\nProcessing account {index + 1}/{total_accounts} - Username: {username}")

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "2315",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "PHPSESSID=3037a73513e8411fbe771513db7e5374",
            "Host": "tonalytics.top",
            "Origin": "https://tonalytics.top",
            "Pragma": "no-cache",
            "Referer": "https://tonalytics.top/",
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "X-Requested-With": "XMLHttpRequest"
        }

        payload = {
            "act": "wheel-spin",
            "account[address]": account['address'],
            "account[walletStateInit]": account['walletStateInit'],
            "account[publicKey]": account['publicKey'],
            "initData": account['initData']
        }

        response = requests.post('https://tonalytics.top/api2.php', headers=headers, data=payload)

        if response.status_code == 200:
            print(f"Success for account {index + 1} - Username: {username}")
        else:
            print(f"Failed for account {index + 1} - Username: {username}, status code: {response.status_code}")

        previous_username = username

        time.sleep(5)  # Delay of 5 seconds between account switches

def main():
    while True:
        process_accounts()
        print("All accounts processed. Starting 7-hour countdown.")
        countdown(7 * 60 * 60)  # 7-hour countdown

if __name__ == "__main__":
    main()
