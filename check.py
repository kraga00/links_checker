from pathlib import Path
import requests
from time import sleep
from random import randint


class LinksReader:
    """Класс для создания списка ссылок из файлов
    """
    def __init__(self):
        """Конструктор класса LiksReader

        Запрашивает:
            Файл с ссылками

        Сохраняет:
            urls_list {list} -- список ссылок
        """
        BASE_DIR = Path(__file__).parent.absolute()
        USER_FILE = input(str('Введите название файла: '))
        file_path = BASE_DIR.joinpath(USER_FILE)

        with open(file_path, 'r') as f:
            self.urls_list = f.read().splitlines()


class UrlChecker:
    """Класс для проверки списков ссылок по разным параметрам
    """
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

    def __init__(self, url_list):
        """Конструктор класса UrlChecker

        Аргументы:
            url_list {list} -- список ссылок
        """
        self.url_list = url_list.urls_list

    def check_status(self):
        """Метод для получения статуса ответов кодов сервера для страниц

        Returns:
            answers_list [list] -- список ссылок с кодом ответов
        """
        answers_list = []

        for url in self.url_list:
            sleep(randint(0, 2))
            resposne = requests.get(url, headers=self.HEADERS)
            status_code = resposne.status_code
            answers_list.append([url, status_code])

        return answers_list


class ListSaver:
    """Класс для сохранения результатов проверки ссылок
    """
    pass
