from requests import Response, get
from bs4 import BeautifulSoup
from shutil import copyfileobj
from time import sleep
from random import randint

from logger import exception
from utils import check_and_create_dir

WEBSITE_URL = 'https://prnt.sc/'
headers = {
    "ACCEPT" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "ACCEPT-LANGUAGE": "en-US,en;q=0.9",
    "DEVICE-MEMORY": "8",
    "DOWNLINK": "10",
    "DPR": "1",
    "ECT": "4g",
    "HOST": "prnt.sc",
    "REFERER": "https://www.google.com/",
    "RTT": "50",
    "SEC-FETCH-DEST": "document",
    "SEC-FETCH-MODE": "navigate",
    "SEC-FETCH-SITE": "cross-site",
    "SEC-FETCH-USER": "?1",
    "UPGRADE-INSECURE-REQUESTS": "1",
    "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "VIEWPORT-WIDTH": "1920",
}

headers_img = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Chromium";v="94", " Not A;Brand";v="99", "Opera GX";v="80"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "UPGRADE-INSECURE-REQUESTS": "1",
    "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "VIEWPORT-WIDTH": "1920",
}
removed_img_links = ['https://i.imgur.com/removed.png']


@exception()
def retry_request(link: str, header: dict, stream: bool = False, times: int = 10):
    page_request = None
    for i in range(times):
        page_request = make_request(link, header, stream)
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
        page_request = retry_request(page_link, headers)
    except ValueError:
        return
    page_soup = get_soup(page_request)
    img_link = get_image_link(page_soup)
    try:
        img_request = retry_request(img_link, headers_img, stream=True)
    except ValueError:
        return
    download_image(img_request, path, filename)
    return


def get_page_link(code: str):
    return WEBSITE_URL + code


def make_request(link: str, header: dict, stream=False):
    page = get(link, headers=header, stream=stream)
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
