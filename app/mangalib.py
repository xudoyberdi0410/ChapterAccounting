# Используется для обхода защиты от ботов на сайте mangalib.me
import cloudscraper
import json
from flask import current_app
import os

class MangaLib():
    def __init__(self):
        """
        Инициализирует класс MangaLib с параметрами по умолчанию.
        Устанавливает базовый URL для API манги, создает экземпляр скраппера,
        инициализирует номер страницы, задает параметры по умолчанию для запросов к API,
        и получает путь к списку манги из конфигурации текущего приложения.
        Atributes:
            _base_url (str): Базовый URL для API манги.
            _scrapper (CloudScraper): Экземпляр CloudScraper.
            _page (int): Текущий номер страницы для пагинации.
            _params (dict): Параметры по умолчанию для запросов к API.
            _path (str): Путь к списку манги из конфигурации приложения.
        """
        
        self._base_url: str = "https://api.mangalib.me/api/manga"
        self._scrapper: cloudscraper.CloudScraper = cloudscraper.create_scraper()
        self._page: int = 1
        self._params: dict[str, any] = {
            "fields[]": ["rate", "rate_avg", "userBookmark"],
            "seed": "8cf96cfb30f43bf7478f43ba8a50641c",
            "site_id[]": 1,
            "target_id": 5064,
            "target_model": "team",
        } # Адрес страницы Dead Inside Team на mangalib.me
        self._path: str = current_app.config['manga_list'] # Путь к списку манги из конфигурации приложения.
    
    def _check_file_exist(self) -> bool:
        """
        Проверяет существует ли файл со списоком тайтлов.
        
        Keyword arguments:
        Return: bool
        """
        
        return os.path.isfile(self._path)

    def update_data(self) -> None:
        """
        Парсит данные из сайта mangalib.me и записывает их в файл
        """
        
        names = []
        while True:
            self._params["page"] = self._page
            response = self._scrapper.get(self._base_url, params=self._params).json()
            if response.get("data"):
                page_data = response.get("data")
                for data in page_data:
                    if data.get("rus_name"):
                        names.append(data.get("rus_name"))
                    else:
                        names.append(data.get("name"))
            self._page += 1
            if response.get("meta").get("has_next_page"):
                continue
            break
        with open(self._path, "w", encoding="utf-8") as file:
            json.dump(names, file, ensure_ascii=False)
    
    def get_manga_list(self) -> list[str]:
        """
        Читает данные из файла и возвращает список тайтлов.
        
        Keyword arguments:
        argument -- description
        Return: list[str]
        """
        
        if not self._check_file_exist():
            self.update_data()
        with open(self._path, 'r', encoding='utf-8') as file:
            manga_list = json.load(file)
        return manga_list
