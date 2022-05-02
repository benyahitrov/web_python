import requests
from bs4 import BeautifulSoup
from typing import List

TARGET_SITE_URL = 'https://www.python.org/'
FILE_NAME = 'output.txt'


def format_url(url: str) -> str:
    if url[0] == '/':
        return f'{TARGET_SITE_URL}{url[1:]}' if len(url) > 1 else TARGET_SITE_URL
    else:
        return url


def url_is_valid(url: str) -> bool:
    if '#' in url:
        return False
    if 'tel:' in url:
        return False
    if 'mailto:' in url:
        return False
    if 'javascript:' in url:
        return False
    if '/' == url:
        return False
    return True


def get_urls(url: str, sublink=True,
             limit=20) -> List:  # Чтобы необходить все ссылки на сайте добавил лимит количества ссылок
    urls = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.find_all("a")
            urls = [format_url(item.get('href')) for item in a_tags if
                    item.get('href') and url_is_valid(item.get('href'))][:limit]
            if sublink:
                urls = [{url_: get_urls(url_, sublink=False, limit=10)} for url_ in urls][:limit]
    except ConnectionError:
        print(f'Connection error')
    finally:
        return urls


def print_urls(urls: List):
    for url in urls:
        for key, value in url.items():
            print(f'{key} ---> {value}')


def write_urls_to_file(urls: List, file_name: str):
    try:
        with open(file_name, 'w') as file:
            for url in urls:
                for key, value in url.items():
                    file.write(f'{key} ---> {value}\n')
    except:
        print('Error writing to file')


def parse_site(output='console'):
    urls = get_urls(TARGET_SITE_URL)
    if output == 'console':
        print_urls(urls)
    elif output == 'file':
        write_urls_to_file(urls, FILE_NAME)


if __name__ == '__main__':
    parse_site()
    parse_site('file')
