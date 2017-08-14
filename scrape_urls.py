
# coding: utf-8

import pandas as pd 
from bs4 import BeautifulSoup
import requests
import time
import sys

url_path = sys.argv[1]
content_path = sys.argv[2]

def get_content(url):
    start = time.time()
    go = True
    i = 1
    content = []
    while(go):
        response = requests.get(url+str(i))
        if i==15:
            go = False
        else:
            content.append(response.content)
        if i % 10 == 0:
            print("Page no. {} downloaded".format(i))
        i += 1 
    num_of_pages = i-1 
    total_time = time.time() - start
    return content, num_of_pages, total_time

def extract_urls_and_names(page):
    lst = []
    soup = BeautifulSoup(page, 'html.parser')
    bots = soup.find_all("div",class_="bot")
    for bot in bots:
        sub_lst = []
        sub_lst.append(bot.find_all('a')[0].get("href"))
        sub_lst.append(bot.find_all('a')[-1].get_text())
        lst.append(sub_lst)
    return lst

def get_names_and_urls(pages):
    lst_total = []
    for page in pages:
        lst_total.append(extract_urls_and_names(page))
    return lst_total

def save_data(path,df):
    df.to_json(path)
    print("Output file saved to: {}".format(path))

def main():

    content,num_pages,tot_time = \
        get_content("https://botlist.co/bots/filter?category=&platform=&order=date&page=")

    print("Downlnoad time in seconds: {}".format(tot_time))
    print("Number of downloaded pages: {}".format(num_pages))

    content_df = pd.DataFrame(content)

    content_df.columns = ["html"]

    content_df["bot_data"] = content_df["html"].apply(extract_urls_and_names)

    pages = content_df.html.values
    names_urls = get_names_and_urls(pages)

    names_urls = sum(names_urls, [])

    bots_df = pd.DataFrame(names_urls)
    bots_df.columns = ["url", "name"]

    save_data(url_path, bots_df)

    save_data(content_path, content_df)

if __name__ == '__main__':
    # print("je")
    main()