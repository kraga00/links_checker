import requests
import argparse

from typing import List, Optional

# в большинстве случаев можно не использовать
HEADERS = {
    'Accept': (
        'text/html,application/xhtml+xml,'
        'application/xml;q=0.9,image/webp,*/*;q=0.8'
    ),
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) '
        'Gecko/20100101 Firefox/76.0'
    )
}


class Link:
    def __init__(self, url: str, status: Optional[int] = None):
        self.url = url
        self.status = status

    def check_status(self):
        try:
            print(f'url {self.url}')
            self.status = requests.get(self.url, headers=HEADERS).status_code
            print(f'status code {self.status}')
        except requests.RequestException as e:
            print(f'Не удалось установить соединение: {e.args[0]}')

    @property
    def prepare_file_line(self):
        return f'{self.url} {self.status}\n'


# В целом тут можно и функциями обойтись
class FileDescriptor:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def read_links_from_file(self) -> List[Link]:
        links = []
        try:
            with open(self.input_path, 'r') as f:
                links = [Link(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            print(f'Файл не найден по пути {self.input_path}')
        return links

    def write_links_to_file(self, links: List[Link]):
        with open(self.output_path, 'w') as f:
            f.writelines(link.prepare_file_line for link in links)


def main():
    parser = argparse.ArgumentParser(description='Link checker')
    parser.add_argument('--path', type=str,
                        help='path to file with links')
    parser.add_argument('--output_path', type=str,
                        help='path to file with links')

    # разбираем входные аргументы
    args = parser.parse_args()
    file_path = args.path
    output_path = args.output_path

    # читаем урлы из файла
    file = FileDescriptor(file_path, output_path)
    links = file.read_links_from_file()

    # проверяем урлы
    if not links:
        print('Пустой файл?')
    for link in links:
        link.check_status()

    # пишем урлы в файл
    file.write_links_to_file(links)


if __name__ == '__main__':
    main()

