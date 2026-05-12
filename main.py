# -*- coding: utf-8 -*-
import requests
import threading
import time
import json
import base64
import urllib.parse
import datetime
import urllib3
import random
import os
import re
import sys

# SSL Warnings বন্ধ করার জন্য
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# CONSTANTS & SETTINGS
# ==========================================
ATOK_FILE_NAME = "accounts.txt"
PROXY_FILE_NAME = "proxies.txt"

DEFAULT_AD_URL = "https://googleads.g.doubleclick.net/mads/gma?submodel=sdk_gphone64_x86_64&adid_p=1&format=interstitial_mb&ini_pn=com.android.vending&ins_pn=com.android.vending&omid_v=a.1.5.2-google_20241009&client_purpose_one=true&dv=260480602&ev=23.6.0&gl=US&hl=en&js=afma-sdk-a-v260480999.244410000.1&lv=244410203&ms=CpgECoACXYpbkGV8iVOSftDAMekBcU_lc2znB9O2_33p3PNwuZHjeNqNwu7HnFKWyJG3rERwi2qIAVthEzc37CNpultvwup6bZzoOCwPw-PikaaFQvF9lLSk1xFPjyzV7_wx2fUHy84d8knN990UY_TzW_oqtf-UDELdQWK7Yj2uBjbZChUrKkDfQAfEbdlgXc5-bSZ4PczAwWRLD8dWcCDxRQ8jSvMm1Jk_sAEMoNK7LaeQvsqTEaVuLdAfs93qtLSICJtYerxNcYP6j7kpB_BHYpyMdzTY2mtUbxjCQ2vRUtrx_ExXdS5LqgXpv5B2vYDVnnY3x5HwD2VbVArHfLX7MkVJEQqAAik5dpcvk0fYk1JEr8godq3Im1WDntsTPBqmPLARb8s0h-yCUhbvdeBVaHKHUrhFuJ8_xJiqBEKwXkjtzibxJLnoo59GGbNbCPoQzLJwV8Kq1kw8TCjUm4MkzFwn9fKfIShF5uf7ue2u2beImjvXlExR6QqAwRpWkrWe8XPKMz3HT3_itEvCQ0AGrEv6EPUISfFs1gJJ1ysVb2_A5iJp5XQwAepbwZOQRe0XohfWg0pA8nzw1mENXrKRLDZtttiBXbEuSn4NwNNcFtDSCJQpa7LFHXrzyqVFj1uEWNlASasygI_zrxx_NRIkBeVOBPu0Bbz_Zy54NolvUw-3H7JchkwSEOOHs7e4hG5rTT4Vlylfqw0SmAQKgAJFz9-ZRHYlOj5ri1E2vJ9e-0vC9Kwjy3YBnTzvlF5O-EcllCD-fVtGkKUuBRNxcEclzxDahifIb9q5OSCoslnoa9jM5lWfEv8kYC7eMmAiQu9Rp959xGj1Vl4Dhkg51su87yvOCMyCSnn1JCwhJJ6q_rPLNB4ecA8Bl-M35JbWWsX6_ePG0r643dxAfYwonbJDqTRpoTF2uRAJIukEiRLxtrJvL2v2hwr7-zFOj5nxyg4cSOZdV4DdDLBzYnM4tD1rUBQ42nINm9BBogW0Tp3a4gOG6-nf4-4WakzslSLYQyaq9p3dWyETAemzg8JDcXnIGjZ9KU8FPTfb9-KNsLUOCoAC0pWCDZhN0COwZZ8-xyZFdjd6n-vsVrq-jM8jPd3B68maF2VXKtYSDw7GFJdD6CbUEn2nrvQAmm-P_hxWB9GLw3N3ebqcEFG34zgtg9eRK7S8kPxRzapRlEarXWqfjJcxMCkfLsza3R3_sD3vEnw6OY_NmvKnsekhqsTuMSApfMvNq9r9ftgiNRVmGfFuI1pJuEHq3yeecdPG2UJBW-xlWC4HP0dkh_570lijaAQ8ckG3QYOV_IKPG7u_g81p4SjM9TZ7SXgardtShPikt3eLlio2BSgQf5B_eHeDvULz2Hnn2dqNIt9GSOG1AgBjGbxP-AmBwxYrlSoze6PNr-euvxIQ94L2kDMkFp-8LHkg3Iatqg&mv=85101930.com.android.vending&lft=1&vnm=1.2.5&plbs=0&plcs=0&risd=1&u_sd=2&request_id=1475162851&sam_b=24&sam_l=0&sam_r=0&sam_t=24&target_api=35&carrier=310260&request_agent=Flutter-GMA-5.3.1&fbs_aeid=-1763672715495716590&fbs_aiid=ed84d026b2efb0c47b9e7545b45685cf&seq_num=65&eid=318500618%2C318486317%2C318491267%2C95389098%2C318509511%2C318514156%2C95388544%2C318483611%2C318484496%2C318484801%2C318526144&guci=0.0.0.0.0.0.0.0&adtest=on&sdk_apis=7%2C8&omid_p=Google%2Fafma-sdk-a-v260480999.244410000.1&u_w=360&u_h=640&msid=com.m2e.mobile&an=123.android.com.m2e.mobile&u_audio=4&net=wi&u_so=p&rbv=1&loeid=44766145%2C318502924&preqs_in_session=2&preqs=64&time_in_session=868530&pcc=0&dload=18229&sst=1777580280000&output=html&region=mobile_app&u_tz=360&client=ca-app-pub-9027478617840640&slotname=9952810315&gsb=wi&apm_app_id=1%3A849245294575%3Aandroid%3A17045a6282e9ba9ab4301a&gmp_app_id=1%3A849245294575%3Aandroid%3A17045a6282e9ba9ab4301a&apm_app_type=1&lite=0&app_wp_code=ca-app-pub-9027478617840640&app_code=9535506442&num_ads=1&vpt=8&vfmt=18&vst=0&sdkv=o.260480999.244410000.1&sdmax=0&dmax=1&sdki=3c4d&stbg=1&bisch=false&blev=0.41&canm=true&_mv=85101930.com.android.vending&heap_free=445936&heap_max=201326592&heap_total=122484208&wv_count=4&advertised_mem_tier=0&avail_mem_tier=0&avail_proc_tier=0&rdps=11650&_cv=261434038&session_idl=20&eo_idl=36&eo_id_tsl=10&is_lat=false&rdidl=36&idtypel=4&blob=ABPQqLEabfpQcA59MgaPX1wtuBt_y7faAofi3bbFnsTYMjvMHAol2Pfu2xBE1dyari8Tpukq3mJ6d3C43sBjZa9dgkovrTzr_REfOnLqNH3LNQqxMcy0HLPBUgNXIleKhnv2eaJhmmL4DQtRAjKR-LSq1ug7tFIY2Jds7YRFkzFQNsJw_gCr_lEBIqPPzZlugiqMctfkSbWSXvkrxRan0zjBb1s0aRHee0rkPybj_jg9vB6BkZhiGUU7DT0hkf8iCVDQvT8TLi0fDYWnxDMOhsdV2K9eGbkv7QhZkIdta3q0kpaCDeWJy_LB3KzUu__ZZbtEiCEOEmhSjMm3nJzntJoogPuVKkYOT116k0GGgrW1ZjVBOYOX1CNkjdj27UIc4tAyEufZUtpeQI4bYb6EIcnpFw_GBoZ759M6mUNj_z8ROzDFs9VCZiWq1nLxGg&capsbf=7FFFFFEE&mr_itag=4509016882487189237_140&jsv=sdk_20190107_RC02-production-sdk_20260423_RC00"
DEFAULT_COOKIE = "IDE=AHWqTUlNM41MtngNvRqYvk3Zj_boF4G4bu69381vQY8AO_81YGGWrHoDR3Qg29sVIjo"
DEFAULT_DRT = "CqwCCqcCRFNJRD1BSUNvaVlQRmgyY3gyaUpxMFNuZnMyVXM2SzMycWd2WTJmUDh6Q2hQdEdqV2NaVTZYQ216WjBUczZnUm9XTGJ6RzFIM2J3SEtNcUc2V3VXWnRCcEtaUTY5NXYzb3NRRVg5dVJ0bjhONkRBazJ4Tnhvckx3bU5PRUdJdXBHNnZQREFyYnZ3aDhIQmp3V1M5NWNRWTg4WnYxakIwLVVRZ1dqY1A2bmEtb1l0NUtMR216a2NGUHNzOW1Ca2lGRGNNWFhqMlJPek9BMy10M191ZEtoMVRwUnQ0UGpOaXk1OFBPQTFpZ2hIdnFzbTV5ZEMtdVRJYVlXaWVuY1dqWVdGUnFTdEZyOGJJTElqZURZcEFtdS1nOFlBYnNSX0FyZWlnNkZhURgB"

BOT_COUNT = 40        # একসাথে ৪০টি থ্রেড চলবে প্রতি একাউন্টের জন্য
BASE_LIMIT = 400      # প্রতি একাউন্টের টার্গেট

# Helper Function
def get_user_id_from_jwt(token):
    try:
        payload = token.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        return str(json.loads(base64.b64decode(payload).decode())['id'])
    except: 
        return None

def safe_log(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

class HeadlessBotManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_success = 0
        self.account_list = []
        self.proxy_list =[]

    def load_accounts(self):
        self.account_list =[]
        if not os.path.exists(ATOK_FILE_NAME):
            safe_log(f"Error: {ATOK_FILE_NAME} not found!")
            return False
            
        with open(ATOK_FILE_NAME, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            email = ""; token = ""
            if "|" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 8:
                    email = parts[1]; token = parts[6].replace("Token:", "").strip()
            else:
                em = re.search(r"Email:\s*(.*?)\s*,", line)
                tk = re.search(r"Token:\s*(.*?)\s*,", line)
                email = em.group(1).strip() if em else ""; token = tk.group(1).strip() if tk else ""
                
            if email and token:
                uid = get_user_id_from_jwt(token)
                if uid:
                    self.account_list.append({"email": email, "token": token, "uid": uid})
                    
        safe_log(f"Loaded {len(self.account_list)} accounts.")
        return len(self.account_list) > 0

    def load_proxies(self):
        self.proxy_list =[]
        if not os.path.exists(PROXY_FILE_NAME):
            safe_log(f"Warning: {PROXY_FILE_NAME} not found! Running without proxies.")
            return

        with open(PROXY_FILE_NAME, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            parts = line.strip().split(":")
            if len(parts) == 4:
                host, port, user, pw = parts
                proxy_url = f"http://{user}:{pw}@{host}:{port}"
                self.proxy_list.append({"http": proxy_url, "https": proxy_url})
                
        safe_log(f"Loaded {len(self.proxy_list)} proxies.")

    def get_atok_data(self, uid):
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        data = {"key": f"{uid}{now}", "type": "MISSION_AD", "missionType": "VIDEO"}
        return urllib.parse.quote(json.dumps(data))

    def bot_worker(self, bot_id, uid, limit):
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15)',
            'X-Requested-With': 'com.m2e.mobile',
            'Cookie': DEFAULT_COOKIE,
            'X-Afma-Drt-V2-Cookie': DEFAULT_DRT,
            'Accept-Encoding': 'gzip'
        }

        while True:
            with self.lock:
                if self.total_success >= limit:
                    break  # টার্গেট পূর্ণ হলে বট স্টপ হয়ে যাবে

            current_proxy = random.choice(self.proxy_list) if self.proxy_list else None
            try:
                response = session.get(DEFAULT_AD_URL, headers=headers, proxies=current_proxy, verify=False, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    ad = data['ad_networks'][0]
                    imp_url = ad['ad']['impression_urls'][0]
                    start_url = ad['video_start_urls'][0]
                    reward_url = ad['video_reward_urls'][0]
                    
                    session.get(imp_url, headers=headers, proxies=current_proxy, verify=False, timeout=15)
                    session.get(start_url, headers=headers, proxies=current_proxy, verify=False, timeout=15)
                    time.sleep(random.randint(6, 8))
                    
                    ts = str(int(time.time() * 1000))
                    cdata = self.get_atok_data(uid)
                    claim_url = reward_url.replace("@gw_rwd_userid@", uid).replace("@gw_tmstmp@", ts).replace("@gw_rwd_custom_data@", cdata)
                    
                    claim_res = session.get(claim_url, headers=headers, proxies=current_proxy, verify=False, timeout=15)
                    if claim_res.status_code == 200:
                        with self.lock:
                            if self.total_success < limit:
                                self.total_success += 1
                                sys.stdout.write(f"\r[+] Bot-{bot_id} Success | Progress: {self.total_success}/{limit} ")
                                sys.stdout.flush()
                else:
                    pass # Ad Fetch Error (Silent for headless)
            except Exception:
                time.sleep(3)
            time.sleep(random.randint(2, 4))

    def process_account(self, index, acc, total_accs):
        uid = acc['uid']
        email = acc['email']
        
        # Dynamic Random Limit Logic (12%)
        variance = max(1, int(BASE_LIMIT * 0.12))
        actual_limit = BASE_LIMIT + random.randint(-variance, variance)
        
        self.total_success = 0
        safe_log(f"\n=========================================")
        safe_log(f"Processing Account {index}/{total_accs}: {email}")
        safe_log(f"Target Limit: {actual_limit} | Concurrent Bots: {BOT_COUNT}")
        safe_log(f"=========================================")

        threads =[]
        for i in range(BOT_COUNT):
            t = threading.Thread(target=self.bot_worker, args=(i+1, uid, actual_limit), daemon=True)
            t.start()
            threads.append(t)
            time.sleep(0.2)  # সার্ভারে একসাথে অতিরিক্ত চাপ না পড়ার জন্য সামান্য গ্যাপ

        # এই একাউন্টের জন্য সবগুলো থ্রেড (বট) শেষ হওয়া পর্যন্ত অপেক্ষা করবে
        for t in threads:
            t.join()
            
        safe_log(f"\n[SUCCESS] Finished Account: {email} | Total Claims: {self.total_success}")
        time.sleep(5)  # পরের একাউন্টে যাওয়ার আগে ৫ সেকেন্ডের বিরতি

    def run_infinite_loop(self):
        cycle = 1
        while True:
            safe_log(f"\n{'='*50}")
            safe_log(f"🚀 STARTING CYCLE NUMBER: {cycle}")
            safe_log(f"{'='*50}")
            
            # প্রতি সাইকেলে একাউন্টের সিরিয়াল রেন্ডম (এলোমেলো) করে নিবে
            random.shuffle(self.account_list)
            total_accs = len(self.account_list)
            
            for index, acc in enumerate(self.account_list, start=1):
                self.process_account(index, acc, total_accs)
                
            safe_log(f"\n✅ [CYCLE {cycle} COMPLETE] All accounts processed.")
            safe_log("Taking a 2 minutes rest before starting the next cycle...")
            time.sleep(120)  # সব একাউন্ট শেষ হলে পরের লুপ শুরু করার আগে ২ মিনিটের রেস্ট
            cycle += 1

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    safe_log("Starting ATOK Headless 24/7 Infinite Bot...")
    
    bot = HeadlessBotManager()
    
    # একাউন্ট এবং প্রক্সি লোড করা
    if bot.load_accounts():
        bot.load_proxies()
        # আনলিমিটেড লুপ শুরু
        bot.run_infinite_loop()
    else:
        safe_log("Bot stopped. Please add valid accounts to accounts.txt")