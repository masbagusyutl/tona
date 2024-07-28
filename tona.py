import os
import time
import requests
import json

# Create accounts directory if it doesn't exist
if not os.path.exists("accounts"):
    os.makedirs("accounts")

def add_account():
    account_data = {}
    account_data['address'] = input("Enter account address: ")
    account_data['walletStateInit'] = input("Enter walletStateInit: ")
    account_data['publicKey'] = input("Enter publicKey: ")
    account_data['initData'] = input("Enter initData: ")
    
    # Manually enter the filename
    filename = input("Enter a name for this account file (without extension): ")

    # Save account data to file
    with open(f"accounts/{filename}.txt", "w") as file:
        json.dump(account_data, file)
    print(f"Account {filename} added successfully!")

def load_accounts():
    accounts = []
    for filename in os.listdir("accounts"):
        if filename.endswith(".txt"):
            with open(os.path.join("accounts", filename), "r") as file:
                account_data = json.load(file)
                account_data['filename'] = filename[:-4]  # Store the filename without extension
                accounts.append(account_data)
    return accounts

def process_account(account, index, total_accounts):
    username = account['filename']
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

    time.sleep(5)  # Delay of 5 seconds between account switches

def countdown_timer(hours):
    total_seconds = hours * 3600
    while total_seconds > 0:
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"\rCountdown: {hours:02}:{minutes:02}:{seconds:02}", end="")
        time.sleep(1)
        total_seconds -= 1
    print("\nCountdown complete. Starting the next round of processing.")

def main():
    while True:
        print("\nMenu:")
        print("1. Add account")
        print("2. Process accounts continuously")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_account()
        elif choice == "2":
            while True:
                accounts = load_accounts()
                total_accounts = len(accounts)
                print(f"Total accounts: {total_accounts}")
                for index, account in enumerate(accounts):
                    process_account(account, index, total_accounts)
                print("\nAll accounts processed. Starting 7-hour countdown.")
                countdown_timer(7)  # 7-hour countdown before processing again
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
