import re, os
from colorama import Fore , Style
from urllib.parse import urlparse
from multiprocessing.dummy import Pool as ThreadPool
def set_cmd_window_size(width, height):
    os.system(f'mode con: cols={width} lines={height}')
set_cmd_window_size(140, 25)
Purple="\033[1;35m"
def LOGO():
    os.system('cls' if os.name == 'nt' else 'clear')
    return fr'''
{Purple}
     ___            ___                  ___                     ___                     
    (   )          (   )                (   )                   (   )                    
  .-.| |    .---.   | |_       .---.     | |    .--.     .---.   | |   ___       .--.    
 /   \ |   / .-, \ (   __)    / .-, \    | |   /    \   / .-, \  | |  (   )    /  _  \   
|  .-. |  (__) ; |  | |      (__) ; |    | |  |  .-. ; (__) ; |  | |  ' /     . .' `. ;  
| |  | |    .'`  |  | | ___    .'`  |    | |  |  | | |   .'`  |  | |,' /      | '   | |  
| |  | |   / .'| |  | |(   )  / .'| |    | |  |  |/  |  / .'| |  | .  '.      _\_`.(___) 
| |  | |  | /  | |  | | | |  | /  | |    | |  |  ' _.' | /  | |  | | `. \    (   ). '.   
| '  | |  ; |  ; |  | ' | |  ; |  ; |    | |  |  .'.-. ; |  ; |  | |   \ \    | |  `\ |  
' `-'  /  ' `-'  |  ' `-' ;  ' `-'  |    | |  '  `-' / ' `-'  |  | |    \ .   ; '._,' '  
 `.__,'   `.__.'_.   `.__.   `.__.'_.   (___)  `.__.'  `.__.'_. (___ ) (___)   '.___.'   
                                                                                         
             By: 221298 | MR.JOKER | https://github.com/vv1ck
    '''

class Filter:
    def __init__(self, target_sites, mode):
        self.target_sites, self.mode = target_sites, mode
        self.total_accounts , self.start_count = 0, 0
        self.saved_accounts = {site: {} for site in target_sites}
        self.account_counts = {site: 0 for site in target_sites}
        while True:
            try:
                with open(input("Enter Combo File: "), 'r', encoding='utf-8') as file:
                    self.lines = file.readlines()
                    break
            except Exception as e:
                print(f"Error reading file: {e}")

        if self.mode == "3":
            self.search_account()
        else:
            self.process_file()

    def extract_domain(self, url):
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path.split('/')[0]
            return domain
        except Exception as e:
            print(f"Error parsing URL {url}: {e}")
            return None

    def is_valid_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  
            r'localhost|'  
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  
            r'(?::\d+)?'  
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    
    def process_line(self, line):
        self.start_count += 1
        try:
            match = re.match(r'^(https?://[^\s:]+|www\.[^\s:]+|[^\s:]+\.[^\s:]+):(.+)$', line)
            if match:
                url = match.group(1)
                account_info = match.group(2)
                for site in self.target_sites:
                    if site in url: 
                        if ':' in account_info:
                            account, password = account_info.split(':', 1)
                            if account in self.saved_accounts[site]:
                                if ' ' in account or ' ' in password:
                                    pass
                                else:
                                    if self.saved_accounts[site][account] != password:
                                        try:
                                            with open(f'saved/{site}.txt', 'a', encoding='utf-8') as domain_file:
                                                domain_file.write(account_info + '\n')
                                            self.saved_accounts[site][account] = password
                                            self.account_counts[site] += 1
                                            self.total_accounts += 1
                                            print(f"\r{Fore.YELLOW}Starting accounts: {self.start_count} | {Fore.GREEN}Total accounts: {self.total_accounts}\r", end="")
                                        except Exception as e:
                                            print(f"\n{Fore.RED}Error writing to file {site}.txt: {e}\n")
                            else:
                                try:
                                    if ' ' in account or ' ' in password:
                                        pass
                                    else:
                                        with open(f'saved/{site}.txt', 'a', encoding='utf-8') as domain_file:
                                            domain_file.write(account_info + '\n')
                                        self.saved_accounts[site][account] = password
                                        self.account_counts[site] += 1
                                        self.total_accounts += 1
                                        print(f"\r{Fore.YELLOW}Starting accounts: {self.start_count} | {Fore.GREEN}Total accounts: {self.total_accounts}\r", end="")
                                except Exception as e:
                                    print(f"\n{Fore.RED}Error writing to file {site}.txt: {e}\n")
                        else:
                            print(f"\r{Fore.YELLOW}Starting accounts: {self.start_count} | {Fore.GREEN}Total accounts: {self.total_accounts}\r", end="")
        except Exception as e:
            print(f"\n{Fore.RED}Unexpected error processing line: {e}\n")


    def process_file(self):
        if not os.path.exists('saved'):
            os.makedirs('saved')
        try:
            with ThreadPool() as pool:
                pool.map(self.process_line, self.lines)
        except KeyboardInterrupt: print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        except Exception as e:
            print(f"\n{Fore.RED}Unexpected error during file processing: {e}\n")
        finally:
            print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            print(self.account_counts)
            print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            print(f"\n{Fore.GREEN}Processing complete.\n")
            input("Press Enter to exit...")

    def search_account(self):
        while True:
            print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            self.search_term = input(f"{Fore.YELLOW}Enter email or username to search: ")
            if self.search_term == '':print(f"{Fore.RED}[-] please enter the search term\n")
            else:
                for line in self.lines:
                    match  = re.match(r'^(https?://[^\s:]+|www\.[^\s:]+|[^\s:]+\.[^\s:]+):(.+)$', line)
                    if match:
                        url = match.group(1)
                        account_info = match.group(2)
                        if self.search_term in account_info:
                            domain = self.extract_domain(url)
                            if domain:
                                print(f"Found in {domain}: {account_info}")
                            elif account_info in self.search_term:
                                print(f"{Fore.GREEN}Found in: {account_info}\n")
                            else:
                                print(f"{Fore.RED}Account not found.\n")
                    
def extract_emails_and_passwords():
    while True:
        file_path = input(f"{Fore.YELLOW}Enter the file path: ")
        if os.path.exists(file_path):
            break
        else:
            print(f"{Fore.RED}File not found. Please try again.\n")
    cont = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(f'emails_{file_path}.txt', 'w') as email_file, open(f'passwords_{file_path}.txt', 'w') as password_file:
        for line in lines:
            cont += 1
            if ':' in line:
                email, password = line.split(':', 1)
                email_file.write(email.strip() + '\n')
                password_file.write(password.strip() + '\n')
            print(f"\r{Fore.YELLOW}Extracting accounts: {cont}", end="")
def filter_accounts():
    while True:
        file_path = input(f"{Fore.YELLOW}Enter the path to the file: ")
        if os.path.exists(file_path):
            break
        else:
            print(f"{Fore.RED}File not found. Please try again.\n")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    unique_accounts = set()
    filtered_lines = []
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) == 2:
            email, password = parts
            if '@' in email:
                if len(password) >= 4:
                    account = (email, password)
                    if account not in unique_accounts:
                        unique_accounts.add(account)
                        filtered_lines.append(line)
    with open('filtered_accounts.txt', 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)


if __name__ == "__main__":
    mode = input(f"{LOGO()}\n{Style.RESET_ALL}1) ~ Extract from one site\n2) ~ Extract from all sites\n3) ~ Search for an account\n4) ~ Extract emails and passwords\n5) ~ Filter accounts\n   [+] Enter the mode [1/2/3/4/5]: ")
    if mode == "1":
        while True:
            target_sites = input(f"{Fore.YELLOW}[+] Enter the target sites: ")
            if target_sites == '':
                print(f"{Fore.RED}[-] please enter the target sites\n")
            else:
                break
        target_sites = [target_sites]
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        Filter(target_sites, mode)
    elif mode == "2":
        target_sites = [
            'instagram', 'facebook', 'snapchat', 'twitter',
            'google', 'discord', 'roblox', 'netflix',
            'shahid', 'tiktok', 'talabat', 'appleid',
            'paypal', 'amazon', 'idmsa', 'twitch',
            'skaraudio', 'shein', 'stake', 'callofduty',
            'sony', 'epicgames', '2captcha', 'roobet',
            'godaddy', 'pythonanywhere', '1xbet',
            'outlook', 'crunchyroll']
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        Filter(target_sites, mode)
    elif mode == "3":
        target_sites = []
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        Filter(target_sites, mode)
    elif mode == "4":
        extract_emails_and_passwords()
    elif mode == "5":
        filter_accounts()
    else:
        print("Invalid mode.")
    input("Press Enter to exit...")