import time
import requests
import urllib.parse
from datetime import datetime, timedelta

# Function to read data from data.txt
def read_data():
    with open('data.txt', 'r') as file:
        lines = file.readlines()
    accounts = []
    for line in lines:
        account_data = {}
        parts = line.strip().split('&')
        for part in parts:
            key, value = part.split('=')
            account_data[key] = urllib.parse.unquote(value)
        accounts.append(account_data)
    return accounts

# Function to send POST request for spinning the wheel
def spin_wheel(account, init_data):
    url = "https://tonalytics.top/api2.php"
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
        "account[address]": account['account[address]'],
        "account[walletStateInit]": account['account[walletStateInit]'],
        "account[publicKey]": account['account[publicKey]'],
        "initDataUnsafe[query_id]": init_data['query_id'],
        "initDataUnsafe[user][id]": init_data['user[id]'],
        "initDataUnsafe[user][first_name]": init_data['user[first_name]'],
        "initDataUnsafe[user][last_name]": init_data['user[last_name]'],
        "initDataUnsafe[user][username]": init_data['user[username]'],
        "initDataUnsafe[user][language_code]": init_data['user[language_code]'],
        "initDataUnsafe[user][is_premium]": init_data['user[is_premium]'],
        "initDataUnsafe[user][allows_write_to_pm]": init_data['user[allows_write_to_pm]'],
        "initDataUnsafe[auth_date]": init_data['auth_date'],
        "initDataUnsafe[hash]": init_data['hash']
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.status_code

# Function to start the 7-hour countdown timer
def countdown_timer(hours=7):
    end_time = datetime.now() + timedelta(hours=hours)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"\rCountdown: {remaining_time}", end="")
        time.sleep(1)
    print("\nCountdown finished. Restarting script...")

# Main function to process all accounts
def main():
    accounts = read_data()
    total_accounts = len(accounts)
    print(f"Total accounts: {total_accounts}")

    for index, account in enumerate(accounts):
        print(f"Processing account {index + 1}/{total_accounts}")
        init_data = {
            "query_id": "example_query_id",
            "user[id]": account['account[address]'],  # Use appropriate field
            "user[first_name]": account['account[walletStateInit]'],  # Use appropriate field
            "user[last_name]": account['account[publicKey]'],  # Use appropriate field
            "user[username]": account['initDataUnsafe[query_id]'],  # Use appropriate field
            "user[language_code]": account['initDataUnsafe[user][id]'],  # Use appropriate field
            "user[is_premium]": account['initDataUnsafe[user][first_name]'],  # Use appropriate field
            "user[allows_write_to_pm]": account['initDataUnsafe[user][last_name]'],  # Use appropriate field
            "auth_date": account['initDataUnsafe[user][username]'],  # Use appropriate field
            "hash": account['initDataUnsafe[user][language_code]']  # Use appropriate field
        }
        status = spin_wheel(account, init_data)
        print(f"Account {index + 1} spin status: {status}")
        time.sleep(5)

    print("All accounts processed. Starting 7-hour countdown.")
    countdown_timer()

if __name__ == "__main__":
    while True:
        main()
