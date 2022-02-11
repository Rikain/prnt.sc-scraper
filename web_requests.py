from requests import Response, get
from bs4 import BeautifulSoup
from shutil import copyfileobj
from time import sleep
from random import randint

from logger import exception
from utils import check_and_create_dir

WEBSITE_URL = 'https://prnt.sc/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
removed_img_links = ['https://i.imgur.com/removed.png']


def retry_request(link: str, stream: bool = False, times: int = 10):
    page_request = None
    for i in range(times):
        page_request = make_request(link, stream)
        if isinstance(page_request, int):
            sleep(2*i + randint(0, 1000) / 1000)
            continue
        break
    if isinstance(page_request, int):
        raise ValueError(page_request)
    return page_request


def download_image_from_code(code: str, filename: str = 'test.png', path: str = 'pictures'):
    page_link = get_page_link(code)
    try:
        page_request = retry_request(page_link)
    except ValueError:
        return
    page_soup = get_soup(page_request)
    img_link = get_image_link(page_soup)
    try:
        img_request = retry_request(img_link, stream=True)
    except ValueError:
        return
    download_image(img_request, path, filename)
    return


def get_page_link(code: str):
    return WEBSITE_URL + code


@exception()
def make_request(link: str, stream=False):
    page = get(link, headers=headers, stream=stream)
    if page.status_code != 200:
        return page.status_code
    else:
        return page


def get_soup(page: Response):
    return BeautifulSoup(page.content, 'html.parser')


def get_image_link(soup: BeautifulSoup):
    return soup.body.img.get('src')


def download_image(page: Response, path: str, filename: str):
    if page.url in removed_img_links:
        return
    check_and_create_dir(path)
    with open(path + '/' + filename, 'wb') as f:
        copyfileobj(page.raw, f)
    return
