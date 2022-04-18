from fastapi import FastAPI, Request
import requests
from bs4 import BeautifulSoup
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


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
        links.append("https://sflix.to"+a['href'])
    return remove_dup(list(filter(lambda k: '/movie/free' in k or "/tv/free" in k, links)))

def get_bflix(search):
    links = []
    page = requests.get(f"https://bflix.gg/search/{search}")
    soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all('a', href=True):
        links.append("https://bflix.gg"+a['href'])
    return remove_dup(list(filter(lambda k: '/movie' in k or "/tv" in k and not "/genre" and not "/tv-show", links)))

def get_movrulz(search):
    links = []
    page = requests.get(f"https://ww5.moviesrulzfree.com/search_movies?s={search}")
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find()
    for a in soup.find_all('a', href=True):
        links.append(a['href'])
    return remove_dup(list(filter(lambda k: 'https://ww5.moviesrulzfree.com/' in k and not "/category" in k and not "/movies" in k and not "/genre" in k and not "/home" in k and not "/language" in k and not "/#" in k and not "/quality" in k, links)))



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    # return {"data":"hello world"}
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search/{search}", response_class=HTMLResponse)
def root(request: Request,search:str):
    return templates.TemplateResponse("search.html", {
        "request": request,
        "search":search,
        "sflix":get_sflix(search),
        "bflix":get_bflix(search),
        "movierulz":get_movrulz(search)
    })

@app.get("/api/v1/{search}")
def root(search:str):
    return {
        "data":{
            "search":search,
            "sflix":get_sflix(search),
            "bflix":get_bflix(search),
            "movierulz":get_movrulz(search)
        }
    }

