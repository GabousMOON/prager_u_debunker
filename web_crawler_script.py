import requests as rq
import bs4 as bs
import selenium as sel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import tldextract as tld
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor


def get_individual_source(link, dataframe):
    sources = {
        "response_code": [],
        "sub_domain": [],
        "domain": [],
        "tld": []
    }
    
    link = link.get_attribute('href')
    subdomain, domain, top_level = tuple(tld.extract(link))
    try:
        sources = dict(zip(sources.keys(), [[rq.get(link).status_code], [subdomain], [domain], [top_level]]))
    except:
        sources = dict(zip(sources.keys(), [['404'], [subdomain], [domain], [top_level]]))
    sources = pd.DataFrame(sources)
    
    pd.concat([dataframe, sources], ignore_index=True)
    
def get_sources(driver, dataframe: pd.DataFrame, video_link: str):
    driver.get(video_link)
    buttons = driver.find_elements('xpath',
                                   "//button[contains(@class, 'box-border inline-flex flex-col items-center justify-center gap-1 rounded-full px-0 py-[.625rem] text-xs font-normal focus:outline-none focus-visible:ring-4 disabled:opacity-60 sm:text-sm xl:flex-row xl:gap-2')]")
    for button in buttons:
        if "Facts &amp; Sources" in button.get_attribute('innerHTML'):
            button.click()
    links = driver.find_elements('xpath',
                                 "//a[contains(@class, 'box-border cursor-pointer items-center justify-center gap-2 rounded-full font-bold focus:outline-none focus-visible:ring-4 py-[.625rem] text-primary hover:opacity-80 focus-visible:ring-neutral-1/25 inline-flex px-0 text-sm')]")
    for link in tqdm(range(len(links))):
        link = links[link]
        row = get_individual_source(link)
        dataframe.loc[len(dataframe.index)] = row
        
def find_links_in_playlist(driver, playlist_link: str):
    driver.get(playlist_link)
    time.sleep(2)
    videos = driver.find_elements('xpath',
                                  "//a[contains(@class, 'grid grid-cols-[142px_1fr] items-center gap-4 overflow-hidden sm:grid-cols-[168px_1fr]')]")
    return videos


def get_sources_of_playlist(driver, play_list_link: 'str', count: int = 0):
    sources = pd.DataFrame({
        "response_code": [],
        "sub_domain": [],
        "domain": [],
        "tld": []
    })

    videos = find_links_in_playlist(driver, play_list_link)

    fixed = []
    for video in videos:
        fixed.append(video.get_attribute('href'))

    
    number = 0
    for video in range(len(fixed)):
        video = fixed[video]
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        get_sources(driver, sources, video)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        number += 1
        if number == count:
            break
    return sources

def main():
    play_list = input('Enter link of playlist: \n')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    sources = get_sources_of_playlist(driver = driver, play_list_link=play_list)
    


if __name__ == 'main':
    main()