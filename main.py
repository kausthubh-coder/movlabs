from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

def remove_dup(arr):
    res = []
    for i in arr:
        if i not in res:
            res.append(i)
    return res

def get_sflix(search):
    links = []
    page = requests.get(f"https://sflix.to/search/{search}")
    soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all('a', href=True):
        links.append(a['href'])
    return remove_dup(list(filter(lambda k: '/movie/free' in k or "/tv/free" in k, links)))

def get_bflix(search):
    links = []
    page = requests.get(f"https://bflix.gg/search/{search}")
    soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all('a', href=True):
        links.append(a['href'])
    return remove_dup(list(filter(lambda k: '/movie' in k or "/tv" in k, links)))

def get_movrulz(search):
    links = []
    page = requests.get(f"https://ww5.moviesrulzfree.com/search_movies?s={search}")
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find()
    for a in soup.find_all('a', href=True):
        links.append(a['href'])
    return remove_dup(list(filter(lambda k: 'https://ww5.moviesrulzfree.com/' in k and not "/category" in k and not "/movies" in k and not "/genre" in k and not "/home" in k and not "/language" in k and not "/#" in k and not "/quality" in k, links)))



app = FastAPI()

@app.get("/")
def root():
    return {"data":"hello world"}

@app.get("/search/{search}")
def root(search:str):
    data = {
        "sflix":get_sflix(search),
        "bflix":get_bflix(search),
        "movie rulz":get_movrulz(search)
    }
    return {"data":data}

