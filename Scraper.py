#! /usr/bin/python

# Web Scraper for Pastebin. Just executes that he downloads the last posts and save in text mode on your PC.
# Author: w00f

import requests
from bs4 import BeautifulSoup
import os
import time
import platform

import requests
from bs4 import BeautifulSoup
import os
import time
import platform

try:
    while True:
        file = open('AccessedSites.txt')
        accessed_sites = file.read()

        pastebin_latest = requests.get('http://pastebin.com/archive')
        pastebin_soup = BeautifulSoup(pastebin_latest.text, 'html.parser')
        table = pastebin_soup.find('table')
        links = []

        for link in table.find_all('a'): 
            if link.get('href') not in accessed_sites and 'archive' not in link.get('href'):
                print('[+] Novo link ', link.get('href'))
                links.append((link.get('href')))

        file.close()
        print('\n')

        if os.path.isdir('Pastebin'):
            print("Starting Download")
        else:
            os.mkdir('Pastebin')
            print("Creating directory and starting download")
        print('\n')

        for content in links:
            print('[+] Downloading http://pastebin.com'+content+'.txt')
            site = requests.get('http://pastebin.com'+content)
            pastebin_download = BeautifulSoup(site.text, 'html.parser')
            title = pastebin_download.find('h1').string
            pastebin_content = pastebin_download.find('textarea')

            if title == 'Untitled':
                title = content

            pastebin = open(os.path.join('Pastebin', os.path.basename(title))+'.txt', 'w', encoding='utf-8')
            contents = pastebin_content.string
            pastebin.write(contents)
            pastebin.close()
        print('\n')

        file = open('AccessedSites.txt', 'a')
        print("[+] Saving accessed links")
        for i in links:
            file.write(i+'\n')
        file.close()

        print('Let\'s return in a minute.')
        print('When you want to stop, use CTRL-C')
        time.sleep(10)
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            os.system('clear')
        elif platform.system() == 'Windows':
            os.system('cls')
        else:
            print('\n'*50)

except KeyboardInterrupt:
    print("\nProgram finished, made by w00f.")
