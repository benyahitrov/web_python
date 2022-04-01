import requests
from bs4 import BeautifulSoup
from typing import List

TARGET_SITE_URL = 'https://www.python.org/'
FILE_NAME = 'output.txt'


def get_urls(url: str, limit=10) -> List:  # Чтобы необходить все ссылки на сайте добавил лимит количества ссылок
    urls = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.find_all("a")
            urls = [item.get('href') for item in a_tags if item.get('href') and 'http' in item.get(
                'href')]  # отфильтровываем локальные ссылки не содержащие протокол
    except:
        print('Network error')
    finally:
        return urls[:limit]


def print_urls(urls: List):
    for url in urls:
        print(url)
        inner_urls = get_urls(url)
        for inner_url in inner_urls:
            print(
                f'####{inner_url}')  # знаки решеток добавил чтобы визуально выделить ссылки которые вложены в первый уровень


def write_urls_to_file(urls: List, file_name: str):
    try:
        with open(file_name, 'w') as file:
            for url in urls:
                file.write(f'{url}\n')
                inner_urls = get_urls(url)
                for inner_url in inner_urls:
                    file.write(f'####{inner_url}\n')
    except:
        print('Error writing to file')


def parse_site(output='console'):
    urls = get_urls(TARGET_SITE_URL)
    if output == 'console':
        # print_urls(urls)
        pass
    elif output == 'file':
        write_urls_to_file(urls, FILE_NAME)


if __name__ == '__main__':
    # parse_site()
    parse_site('file')
