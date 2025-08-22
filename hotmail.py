# ====== CREATED BY Fahdii======
import os
import random
import string
import hashlib
import re 
import time
from datetime import datetime
from faker import Faker
from colorama import Fore, Back, Style, init
import uuid
import platform
import subprocess

# Initialize colorama
init(autoreset=True)

try:
    import requests
except:
    os.system('python -m pip install requests')
    import requests

try:
    from bs4 import BeautifulSoup
except:
    os.system('python -m pip install beautifulsoup4')
    from bs4 import BeautifulSoup

# ====== DEVICE LOCK SYSTEM ======
def get_device_fingerprint():
    """Generate a consistent hardware-based fingerprint for the device"""
    try:
        # Get system information that's unique to the device
        info = {
            'machine': platform.machine(),
            'node': platform.node(),
            'processor': platform.processor(),
            'system': platform.system(),
            'release': platform.release()
        }
        
        # For Windows - get disk serial
        if platform.system() == 'Windows':
            try:
                disk_serial = subprocess.check_output("wmic diskdrive get serialnumber", shell=True).decode().split('\n')[1].strip()
                info['disk'] = disk_serial
            except:
                pass
        # For Linux/Mac - get machine-id
        else:
            try:
                with open('/etc/machine-id', 'r') as f:
                    info['machine_id'] = f.read().strip()
            except:
                try:
                    with open('/var/lib/dbus/machine-id', 'r') as f:
                        info['machine_id'] = f.read().strip()
                except:
                    pass
        
        # Create a stable hash of all this information
        fingerprint_str = ''.join(f"{k}:{v}" for k,v in sorted(info.items()))
        fingerprint = hashlib.sha256(fingerprint_str.encode()).hexdigest()
        
        # Format as a key (first 16 chars of hash)
        device_key = f"DEV-{fingerprint[:16].upper()}"
        return device_key
        
    except Exception as e:
        # Fallback if any error occurs
        fallback_id = str(uuid.getnode())
        return f"FALLBACK-{hashlib.sha256(fallback_id.encode()).hexdigest()[:16]}"

# Updated approval system with better error handling and fallback
def check_approval():
    """Check if device is approved - strictly online verification"""
    device_key = get_device_fingerprint()
    
    print(f"{Fore.YELLOW}\n🔒 Checking Device Authorization...")
    time.sleep(1)
    
    # Try multiple GitHub URLs
    github_urls = [
        "https://raw.githubusercontent.com/fahdii51/TEMP_MAIL/main/Approval.txt",
        "https://github.com/fahdii51/TEMP_MAIL/blob/main/Approval.txt",
        "https://bitbucket.org/fahdii51/TEMP_MAIL/raw/main/Approval.txt"
    ]
    
    for url in github_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                approved_keys = [k.strip() for k in response.text.splitlines() if k.strip()]
                
                if device_key in approved_keys:
                    print(f"{Fore.GREEN}✅ Device Approved! Loading Tool...")
                    os.system('clear')
                    print(logo)
                    time.sleep(1)
                    return True
                else:
                    print(f"{Fore.RED}⛔ Device Not Authorized!")
                    print(f"{Fore.CYAN}\nYour Device Key: {Fore.WHITE}{device_key}")
                    print(f"{Fore.YELLOW}\nPlease send this key to the tool owner to get access")
                    print(f"{Fore.YELLOW}\nWhatsapp :- +923093601043 📨")
                    print(f"{Fore.MAGENTA}\nPress Enter to exit...")
                    input()
                    return False
        except requests.exceptions.RequestException as e:
            continue
    
    # If all URLs failed
    print(f"{Fore.RED}⛔ Authorization Failed!")
    print(f"{Fore.CYAN}\nYour Device Key: {Fore.WHITE}{device_key}")
    print(f"{Fore.YELLOW}\nPlease ensure you have internet connection and try again.")
    print(f"{Fore.YELLOW}\nWhatsapp :- +923093601043 📨")
    print(f"{Fore.MAGENTA}\nPress Enter to exit...")
    input()
    return False

# ------------[ COLORS ]-------------- #
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
RESET = '\033[0m'
WHITE = '\033[1;37m'

# ------------[ BANNER ]-------------- #
run_count = 0

status_list = ['Online', 'Active', 'Busy', 'Away', 'Do Not Disturb']
random_status = random.choice(status_list)

W = "\x1b[97m"
G = "\x1b[38;5;46m"
R = "\x1b[38;5;196m"
Y = "\x1b[33m"
B = "\x1b[34m"
X = f"{W}<{R}•{W}>"

logo = f'''
{R}________________    ___ ___    _____  ________   
{R}\\_   _____/  _  \\  /   |   \\  /  _  \\ \\______ \\  
{R} |    __)/  /_\\  \\/    ~    \\/  /_\\  \\ |    |  \\ 
{R} |     \\/    |    \\    Y    /    |    \\|    `   \\
{R} \\___  /\\____|__  /\\___|_  /\\____|__  /_______  /
{R}    \\/         \\/       \\/         \\/        \\/ 
{W}──────────────────────────────────────────────────
{W}[+] Owner    : {GREEN}Fahdii{WHITE}
{W}[+] Facebook : {GREEN}Not registered {WHITE}
{W}[+] Status   : {GREEN}{random_status}{WHITE}
{W}[+] Github   : {YELLOW}Auto Create{WHITE}
{W}[+] Version  : 0.1
{W}[+] Run Count: {run_count}
{W}──────────────────────────────────────────────────
'''

# ------------[ HELPERS ]-------------- #
def clear():
    os.system('clear')
    print(logo)

def linex():
    print(WHITE + '=' * 45)

#-------------HOTMAILS--------------#

def get_latest_message_code(email, refresh_token, client_id):
    """
    Fetch messages via dongvanfb API and extract the latest Facebook code if available.
    """
    try:
        url = "https://tools.dongvanfb.net/api/get_messages_oauth2"
        payload = {
            "email": email,
            "refresh_token": refresh_token,
            "client_id": client_id
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, json=payload, headers=headers, timeout=40)
        if r.status_code == 200:
            data = r.json()
            # Messages array
            messages = data.get("messages", [])
            for msg in messages:
                if msg.get("code"):
                    return msg["code"]   # return first found code
        return None
    except Exception as e:
        print(Fore.RED + f"[✗] Error fetching code: {e}")
        return None
        
def load_ms_accounts(path):
    """
    Load hotmail accounts from a file.
    Each line: email|password|refresh_token|client_id
    Returns list of dicts.
    """
    accounts = []
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    email, password, refresh_token, client_id = parts
                    accounts.append({
                        "email": email,
                        "password": password,
                        "refresh_token": refresh_token,
                        "client_id": client_id
                    })
                else:
                    print(Fore.RED + f"[!] Skipping malformed line: {line.strip()}")
        return accounts
    except FileNotFoundError:
        print(Fore.RED + f"[✗] File not found: {path}")
        return []
        

# ====== USER AGENT GENERATOR ======
def ua1():
    a = "[FBAN/FB4A;FBAV/"+str(random.randint(11,80))+'.0.0.'+str(random.randrange(9,49))+'.'+str(random.randint(11,77)) +";FBBV/"+str(random.randint(11111111,99999999))+";"
    b = "[FBAN/FB4A;FBAV/309.0.0.47.119;FBBV/277444756;FBDM/{density=3.0,width=1080,height=1920};FBLC/de_DE;FBRV/279865282;FBCR/Willkommen;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-N770F;FBSV/10;FBOP/19;FBCA/armeabi-v7a:armeabi;]"
    ua1 = a+b
    return ua1

def ua2():
    a = "[FBAN/FB4A;FBAV/"+str(random.randint(11,80))+'.0.0.'+str(random.randrange(9,49))+'.'+str(random.randint(11,77)) +";FBBV/"+str(random.randint(11111111,99999999))+";"
    b = "[FBAN/FB4A;FBAV/365.0.0.30.112;FBBV/367653576;FBDM/{density=2.25,width=720,height=1400};FBLC/en_Qaau_US;FBRV/369757394;FBCR/Vi India;FBMF/Realme;FBBD/Realme;FBPN/com.facebook.katana;FBDV/RMX1945;FBSV/9;FBOP/1;FBCA/arm64-v8a:;]"
    ua2 = a+b
    return ua2

def ua3():
    a = "[FBAN/FB4A;FBAV/"+str(random.randint(11,80))+'.0.0.'+str(random.randrange(9,49))+'.'+str(random.randint(11,77)) +";FBBV/"+str(random.randint(11111111,99999999))+";"
    b = "[FBAN/FB4A;FBAV/280.0.0.48.122;FBBV/233235247;FBDM/{density=3.0,width=1080,height=2132};FBLC/en_US;FBRV/235412020;FBCR/airtel;FBMF/OPPO;FBBD/OPPO;FBPN/com.facebook.katana;FBDV/CPH1893;FBSV/9;FBOP/1;FBCA/armeabi-v7a:armeabi;]"
    ua3 = a+b
    return ua3

def ua4():
    a = "[FBAN/FB4A;FBAV/"+str(random.randint(11,80))+'.0.0.'+str(random.randrange(9,49))+'.'+str(random.randint(11,77)) +";FBBV/"+str(random.randint(11111111,99999999))+";"
    b = "[FBAN/FB4A;FBAV/257.0.0.44.118;FBBV/197851411;FBDM/{density=3.0,width=1080,height=2118};FBLC/en_US;FBRV/199646485;FBCR/Jio 4G;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/vivo 1951;FBSV/9;FBOP/1;FBCA/arm64-v8a:;]"
    ua4 = a+b
    return ua4

def ua5():
    a = "[FBAN/FB4A;FBAV/"+str(random.randint(11,80))+'.0.0.'+str(random.randrange(9,49))+'.'+str(random.randint(11,77)) +";FBBV/"+str(random.randint(11111111,99999999))+";"
    b = "[FBAN/FB4A;FBAV/365.0.0.30.112;FBBV/367653576;FBDM/{density=2.25,width=720,height=1400};FBLC/en_Qaau_US;FBRV/369757394;FBCR/Vi India;FBMF/Realme;FBBD/Realme;FBPN/com.facebook.katana;FBDV/RMX1945;FBSV/9;FBOP/1;FBCA/arm64-v8a:;]"
    ua5 = a+b
    return ua5

def ua():
    p1 = ua1()
    p2 = ua2()
    p3 = ua3()
    p4 = ua4()
    p5 = ua5()
    ua = random.choice([p1,p2,p3,p4,p5])
    return ua

# ====== EMAIL GENERATOR ======

def generate_random_pakistani_number():
    # Pakistan country code +92
    # Select a random valid operator code
    operator_codes = ['300', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310',
                      '311', '312', '313', '314', '315', '316', '317', '318', '319', '320', '321',
                      '322', '323', '324', '325', '326', '327', '328', '329', '330', '331', '332',
                      '333', '334', '335', '336', '337', '338']
    operator = random.choice(operator_codes)
    # Generate the 7-digit subscriber number
    subscriber_number = ''.join(random.choices(string.digits, k=7))
    phone_number = f"+92{operator}{subscriber_number}"
    return phone_number
    
# ====== LOCK CHECK ======
def lock_checker(uid):
    try:
        r = requests.get(f'https://graph.facebook.com/{uid}/picture?type=normal', timeout=10)
        return 'Active' if 'Photoshop' in r.text else 'Locked'
    except:
        return 'Error'

# ====== RANDOM STRING ======
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ====== REGISTER FUNCTION ======
def register_facebook_account(password, first_name, last_name, birthday, email, refresh_token, client_id):
    session = requests.Session()
    
    headers = {'User-Agent': ua()}
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    
    is_phone = email.startswith('+')
    
    req = {
        'api_key': api_key,
        'attempt_login': True,
        'birthday': birthday.strftime('%Y-%m-%d'),
        'client_country_code': 'US',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': first_name,
        'format': 'json',
        'gender': gender,
        'lastname': last_name,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': generate_random_string(32),
        'return_multiple_errors': True
    }
    
    if is_phone:
        req['phone'] = email
    else:
        req['email'] = email

    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig

    try:
        response = session.post('https://b-api.facebook.com/method/user.register', data=req, headers=headers)
        reg = response.json()
        uid = reg.get('new_user_id')
        if uid:
            status = lock_checker(uid)
            if status == 'Active':
                time.sleep(5)
                if not is_phone and refresh_token and client_id:
                    try:
                        code = get_latest_message_code(email, refresh_token, client_id)
                        if code:
                            confirm_url = 'https://b-api.facebook.com/method/auth.confirm_email'
                            payload = {
                                'email': email,
                                'code': code,
                                'format': 'json',
                                'access_token': reg.get('session_info', {}).get('access_token', '')
                            }
                            confirm = session.post(confirm_url, data=payload, headers=headers)
                            print(Fore.GREEN + f"[✓] Verified: {email} with code {code}")
                        else:
                            print(Fore.RED + "[✗] Could not fetch verification code")
                    except Exception as e:
                        print(Fore.RED + f"[✗] Verification error: {e}")

                with open("SUCCESS-OK-ID.txt", "a") as f:
                    f.write(f"{uid}|{password}|{email}\n")
                
                print(Fore.GREEN + """
╔══════════════════════════════════════════════╗
║            ACCOUNT CREATED SUCCESSFULLY      ║
╠══════════════════════════════════════════════╣""")
                print(Fore.CYAN + f"""║ {Fore.YELLOW}• EMAIL{Fore.RESET}    : {Fore.WHITE}{email.ljust(32)}║
║ {Fore.YELLOW}• UID{Fore.RESET}      : {Fore.WHITE}{str(uid).ljust(32)}║
║ {Fore.YELLOW}• PASSWORD{Fore.RESET} : {Fore.WHITE}{password.ljust(32)}║
║ {Fore.YELLOW}• NAME{Fore.RESET}     : {Fore.WHITE}{(first_name + ' ' + last_name).ljust(32)}║
║ {Fore.YELLOW}• BIRTHDAY{Fore.RESET} : {Fore.WHITE}{str(birthday).ljust(32)}║
║ {Fore.YELLOW}• GENDER{Fore.RESET}   : {Fore.WHITE}{gender.ljust(32)}║
╚══════════════════════════════════════════════╝
""")
                return True
            else:
                print(Fore.RED + '[✗] ID Locked')
                return False
        else:
            print(Fore.RED + '[✗] Account Disabled or Failed')
            return False
    except Exception as e:
        print(Fore.RED + f'[✗] Error: {e}')
        return False

# ====== MAIN ======




def create_account_both_steps(password, first_name, last_name, birthday, hotmail_email, refresh_token, client_id):
    """Create the same account first with random number, then with Hotmail email."""

    # Step 1: Create with random number (silent mode, no details shown)
    random_number = generate_random_pakistani_number()
    print(Fore.BLUE + f"[•] Creating temporary ID with random number: {random_number}")
    register_facebook_account(password, first_name, last_name, birthday, random_number, None, None)

    # Clear screen so random number result disappears
    os.system('clear')
    print(logo)

    # Step 2: Create with Hotmail (show details)
    print(Fore.BLUE + f"[•] Now creating with Hotmail: {hotmail_email}")
    success = register_facebook_account(password, first_name, last_name, birthday, hotmail_email, refresh_token, client_id)

    if success:
        code = get_latest_message_code(hotmail_email, refresh_token, client_id)
        if code:
            print(Fore.GREEN + f"[✓] OTP for {hotmail_email}: {code}")
        else:
            print(Fore.RED + f"[✗] Could not fetch OTP for {hotmail_email}")


# ====== MAIN ======
def main():
    os.system('clear')
    print(logo)

    if not check_approval():
        exit()

    fake = Faker()

    # Ask for hotmails.txt path
    path = input(Fore.BLUE + "\nEnter path to hotmails/outlooks file: ").strip()
    accounts = load_ms_accounts(path)

    if not accounts:
        print(Fore.RED + "[✗] No valid accounts loaded!")
        exit()

    print(Fore.YELLOW + f"\n[+] Loaded {len(accounts)} Microsoft (Hotmail/Outlook) accounts from file")

    # Ask for manual password
    manual_password = input(Fore.CYAN + "\nEnter password to use for all accounts: ").strip()

    for idx, acc in enumerate(accounts, start=1):
        print(Fore.YELLOW + "\n" + "="*60)
        print(Fore.CYAN + f"ACCOUNT {idx} OF {len(accounts)}".center(60))
        print(Fore.YELLOW + "="*60)

        hotmail_email = acc["email"]
        refresh_token = acc["refresh_token"]
        client_id = acc["client_id"]

        # Fake details
        fname = fake.first_name()
        lname = fake.last_name()
        bday = fake.date_of_birth(minimum_age=18, maximum_age=28)

        # Create same account in both steps (first random, then Hotmail)
        create_account_both_steps(manual_password, fname, lname, bday, hotmail_email, refresh_token, client_id)

        if idx < len(accounts):
            time.sleep(2)


if __name__ == "__main__":
    main()