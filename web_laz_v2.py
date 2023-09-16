import requests, json, time, random, sqlite3, threading, datetime

api_laz = 'https://api.telegram.org/bot6061425394:AAGgUbb_DNvy9WiS0cP3yQGv1dciasJipX4/sendMessage'
api_pee = 'https://api.telegram.org/bot6201906509:AAHS_bUNOcQJNQHv9TEShzarFPMw1-IAVoY/sendMessage'
chat_id =  -1001937367940 #1869003650 #-824765139

def tele(mess, api):
        requests.post(
                    api,
                    json={
                        'chat_id': chat_id,
                        'text': mess,
                        'parse_mode': 'Markdown',
                        'disable_web_page_preview': True
                    }
            )
def add_sent(code):
    conn = sqlite3.connect("sent_laz_v2.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO sent_codes (code) VALUES (?)", (code,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False
def create_table():
    conn = sqlite3.connect("sent_laz_v2.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sent_codes (
            code TEXT PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

def check_sent_codes():
    conn = sqlite3.connect("sent_laz_v2.db")
    cursor = conn.cursor()

    cursor.execute("SELECT code FROM sent_codes")
    sent_codes = [row[0] for row in cursor.fetchall()]

    conn.close()
    return sent_codes

def laz():
    url = "https://api.bloggiamgia.vn/api/b/Voucher/home-lazada"

    payload = {}
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Origin': 'https://bloggiamgia.vn',
    'Referer': 'https://bloggiamgia.vn/',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    #print(response.text)
    data = json.loads(response.text)
    coupon_codes = [coupon["couponCode"] for coupon in data["data"] if coupon["couponCode"] != ""]
    sl = len(coupon_codes)
    print(f"SL Laz: {sl}")
    #time.sleep(delay)
    coupon_details = [{"couponCode": coupon["couponCode"], "title": coupon["title"], "note": coupon["note"]} for coupon in data["data"] if coupon["couponCode"]]
    sent_codes = check_sent_codes()

    # Print the coupon codes, titles, and notes
    for coupon in coupon_details:
        code, title, note = coupon["couponCode"], coupon["title"], coupon["note"]
        if code not in sent_codes:
            mess = f"*🔥 Code:    *`{code}`\n\n*► Title: *{title}\n*► Note: *{note}\n\n*🛒    https://cart.lazada.vn/cart*"
            tele(mess, api_laz)
            add_sent(code)

def run_laz(delay):
    n = 2
    while True:
        laz()
        print(f"{n}. ({datetime.datetime.now().strftime('%H:%M:%S')}) Đang chờ trong {delay} giây...")
        time.sleep(delay)
        n +=1
create_table()

tg=list(map(int,input("Random: ").split()))
delay = random.randint(tg[0], tg[1])

thread_laz = threading.Thread(target=run_laz, args=(delay,))
thread_laz.start()
thread_laz.join()