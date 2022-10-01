from bs4 import BeautifulSoup
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time

s = Service(r'C:\Users\reshv\Desktop\education\some python tricks\Internet\chromedriver.exe')


def movie_selector(genre=None, mode=None, *, random_movie=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3"}

    base_url = ("https://www.imdb.com/search/title/?groups=top_1000")
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    movies = soup.find_all(class_='lister-item mode-advanced')

    for i in range(51, 152, 50):
        url = base_url + f'&start={str(i)}&ref_=adv_nxt'
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        movies.extend(soup.find_all(class_='lister-item mode-advanced'))

    if random_movie:
        pass

    movies = [movie for movie in movies if genre in movie.find(class_='genre').text]
    if mode == 'all-times-best':
        movies.sort(key=lambda x: x.find(class_='inline-block ratings-imdb-rating').strong.text, reverse=True)
    if mode == 'most recent':
        movies = [movie for movie in movies if
                  movie.find(class_='lister-item-year text-muted unbold').text in ['2021', '2022']]
        random.shuffle(movies)
    if mode == 'random':
        random.shuffle(movies)
    movies = movies[:3]
    dict_to_return = dict()
    for movie in movies:
        url = "https://www.imdb.com" + movie.find(class_='lister-item-header').a.get('href')
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        name = soup.find(class_='sc-80d4314-1 fbQftq').find('h1').text
        dict_to_return[name] = list()
        dict_to_return[name].append("https://www.imdb.com" + soup.find(
            class_='ipc-lockup-overlay sc-f0d4a9ac-2 gkiDbj hero-media__slate-overlay ipc-focusable').get('href'))
        url = "https://filmix.ac/search/" + name.strip().replace(" ", '%20')
        driver = webdriver.Chrome(service=s)
        driver.get(url)
        try:
            time.sleep(3)
            driver.find_element(by=By.XPATH, value='// *[ @ id = "filtersForm"] / div[9] / input').click()
            time.sleep(3)
            href = driver.find_element(by=By.XPATH, value='//*[@id="searchtable"]/article/div[1]/a').get_attribute(
                'href')
        except:
            href = ""
        finally:
            driver.close()
        dict_to_return[name].append(href)
    return dict_to_return

