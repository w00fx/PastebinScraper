#! /usr/bin/python

# Web Scraper for Pastebin.
# Just executes that he downloads the last posts and save in text mode on your PC.
# Author: w00f

import platform
import os
import sys
import time
import re
import requests
from bs4 import BeautifulSoup

def ac_sites(link_list):
    if not os.path.exists(link_list):
        file = open(link_list, 'w')
        file.write('Accessed links\n\n')
        try:
            global cont
            cont = file.read()
        except IOError:
            ac_sites(link_list)
        file.close()
        return cont
    else:
        file = open(link_list)
        cont = file.read()
        file.close()
        return cont


def check_directory(arg):
    if os.path.isdir('Pastebin/'+arg):
        print("Starting Download")
    else:
        os.makedirs('Pastebin/'+arg)
        print("Creating directory and starting download")


def get_links(soup):
    table = soup.find('table')
    links = []
    for link in table.find_all('a'):
        if link.get('href') not in accessed_sites and not re.search(
                r'\b[a-zA-Z0-9]{8}\b', link.get('href'), re.IGNORECASE) == None:
            print('[+] New link ', link.get('href'))
            links.append((link.get('href')))
    return links


def download_contents(link,arg):
    print('[+] Downloading http://pastebin.com'+link+'.txt')
    site = requests.get('http://pastebin.com'+link)
    pastebin_download = BeautifulSoup(site.text, 'html.parser')
    title = pastebin_download.find('h1').string
    pastebin_content = pastebin_download.find('textarea')
    if title == 'Untitled':
        title = content
    try:
        pastebin = open(os.path.join
                        ('Pastebin/'+arg, os.path.basename(title))+'.txt', 'w', encoding='utf-8')
    except:
        pastebin = open(os.path.join
                        ('Pastebin/'+arg, os.path.basename('Untitled'))+'.txt', 'w', encoding='utf-8')
    contents = pastebin_content.string
    pastebin.write(contents)
    pastebin.close()


def saving_links(text_name, link_list):
    file = open(text_name, 'a')
    print("[+] Saving accessed links")
    for i in link_list:
        file.write(i+'\n')
    file.close()


try:
    print('[+] Downloading Trends')
    accessed_sites = ac_sites('Trends_Accessed_Links.txt')
    pastebin_latest = requests.get('http://pastebin.com/trends')
    pastebin_soup = BeautifulSoup(pastebin_latest.text, 'html.parser')
    print('[+] Getting links')
    latest_links = get_links(pastebin_soup)
    print('\n')
    check_directory('TrendContents')
    print('[+] Downloading trends content...')
    for content in latest_links:
        download_contents(content, 'TrendContents')
    print('\n')
    print('[+] Saving Links')
    saving_links('Trends_Accessed_Links.txt', latest_links)
    print('\n\n')

    while True:
        accessed_sites = ac_sites('Last_Accessed_Links.txt')
        pastebin_latest = requests.get('http://pastebin.com/archive')
        pastebin_soup = BeautifulSoup(pastebin_latest.text, 'html.parser')
        latest_links = get_links(pastebin_soup)

        print('\n')
        check_directory('LastContent')

        for content in latest_links:
            download_contents(content, 'LastContent')

        print('\n')
        saving_links('Last_Accessed_Links.txt', latest_links)

        print('Let\'s return in a minute.')
        print('When you want to stop, use CTRL-C')
        time.sleep(60)
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            os.system('clear')
        elif platform.system() == 'Windows':
            os.system('cls')
        else:
            print('\n'*50)

except KeyboardInterrupt:
    print("\nProgram finished, made by w00f.")
