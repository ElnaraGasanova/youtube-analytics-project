import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # id канала
        self.__channel_id = channel_id
        # данные по каналу
        self.channel_info = Channel.take_dict_to_print(self.__channel_id)
        # название канала
        self.title = self.channel_info['items'][0]['snippet']['title']
        # описание канала
        self.description = self.channel_info['items'][0]['snippet']['description']
        # ссылка на канал
        self.url = "https://www.youtube.com/channel/" + self.channel_info['items'][0]['snippet']['customUrl']
        # количество подписчиков
        self.subscribers_count = int(self.channel_info['items'][0]['statistics']['subscriberCount'])
        # количество видео
        self.video_count = int(self.channel_info['items'][0]['statistics']['videoCount'])
        # общее количество просмотров
        self.view_count = int(self.channel_info['items'][0]['statistics']['viewCount'])

    # Данный декоратор прописан для того, что вывести ошибку, согласно задания.
    # @property
    # def channel_id(self):
    #     return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        channel_print_info = json.dumps(channel, indent=2, ensure_ascii=False)
        print(channel_print_info)
        # print(self.channel_print_info)

    @classmethod
    def take_dict_to_print(cls, channel_id: str) -> dict:
        """
        создает словарь с данными по каналу
        :returns: Dictionary with info about the channel
        """
        channel_info = cls.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return channel_info

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        new_object_ytapi = Channel.youtube
        return new_object_ytapi

    def to_json(self, filename: str) -> None:
        """Cоздает файл 'filename' с данными по каналу"""
        data = {
            'id_канала': self.__channel_id,
            'название_канала': self.title,
            'описание_канала': self.description,
            'ссылка_на_канал': self.url,
            'количество_подписчиков': self.subscribers_count,
            'количество_видео': self.video_count,
            'общее_количество_просмотров': self.view_count
        }
        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    # def to_json(self, filename: str) -> None:
    #     """Cоздает файл 'filename' с данными по каналу"""
    #     with open(filename, 'w', encoding='utf-8') as file:
    #         file.write(json.dumps(self.channel_info, indent=2, ensure_ascii=False))
