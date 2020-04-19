import requests
from collections import deque
import os
import sys
from bs4 import BeautifulSoup
from colorama import *

init()

web_extensions = ['com', 'org', 'net', 'io', 'ro']

# Creation of a directory in which to store tabs
args = sys.argv
directory_name = args[1]
if not os.path.exists(directory_name):
    os.mkdir(directory_name)

# Stack used to implement back functionality
stack = deque()

while True:
    auxiliary_url = input()
    stack.append(auxiliary_url)
    split_url = auxiliary_url.split('.')
    url_for_path = ''
    if len(split_url) > 2:
        for i in range(0, len(split_url) - 1):
            if i < len(split_url)-2:
                url_for_path += split_url[i] + '.'
            else:
                url_for_path += split_url[i]
    else:
        url_for_path = split_url[0]
    file_name = url_for_path + '.txt'
    file_path = os.path.join(directory_name, file_name)
    if auxiliary_url.lower() == 'exit':
        sys.exit(0)

    if auxiliary_url.lower() == 'back':
        if len(stack) > 1:
            stack.pop()
            stack.pop()
            auxiliary_url = stack.pop()
        else:
            pass

    extension = auxiliary_url.split('.')[-1]
    if extension in web_extensions:
        url = "http://" + auxiliary_url
        try:
            response = requests.get(url)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            # get text
            text = soup.get_text()
            print(Fore.BLUE + text)
            # If the URL is correct, keep this site open in a tab
            with open(file_path, 'w+') as file:
                file.write(text)
        except requests.ConnectionError as exception:
            print("ERROR: Invalid URL! Please try again...")
    else:
        if os.path.exists(file_path):
            with open(file_path, 'r+') as file:
                contents = file.read()
                print(contents)
        else:
            print("ERROR: Invalid URL! Please try again...")
