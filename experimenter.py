import requests
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
from bs4 import BeautifulSoup
import csv


driver = webdriver.Chrome(ChromeDriverManager().install())

def get_sources(driver, video_link: str):
    driver.get(video_link)
    buttons = driver.find_elements('xpath',
                                "//button[contains(@class, 'box-border inline-flex flex-col items-center justify-center gap-1 rounded-full px-0 py-[.625rem] text-xs font-normal focus:outline-none focus-visible:ring-4 disabled:opacity-60 sm:text-sm xl:flex-row xl:gap-2')]")
    for button in buttons:
        if "Facts &amp; Sources" in button.get_attribute('innerHTML'):
            button.click()
    links = driver.find_elements('xpath',
                                "//a[contains(@class, 'box-border cursor-pointer items-center justify-center gap-2 rounded-full font-bold focus:outline-none focus-visible:ring-4 py-[.625rem] text-primary hover:opacity-80 focus-visible:ring-neutral-1/25 inline-flex px-0 text-sm')]") 
    links = [link.get_attribute('href') for link in links]
    return links



with open ('test_sources.csv', 'w') as test_file:
    test_writer = csv.writer(test_file)
        
    def parse_page(url):
        # perform the HTTP request to the specified URL
        try:
            response = requests.get(url)
        except:
            response = '404'
        extracted = tld.extract(url)
        test_writer.writerow([extracted.subdomain, extracted.domain, extracted.suffix, response])
    
    urls = get_sources(driver,
            'https://www.prageru.com/video/theodore-roosevelt-the-action-hero-president?playlist=american-presidents')
    
    # max number of threads to use
    MAX_THREADS = 4

    # initialize ThreadPoolExecutor and use it to call parse_page() in parallel
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(parse_page, urls)
    
    
