import os
from googleapiclient.discovery import build


class Video:

    def __init__(self, channel_id: str, youtube = build('youtube', 'v3',
                                                        developerKey=os.getenv('API_KEY'))) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""

        # id канала
        self.channel_id = channel_id
        self.youtube = youtube
        # ссылка на видео
        self.channel = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=channel_id
                                       ).execute()
        # название
        self.title = self.channel['items'][0]['snippet']['title']
        # количество просмотров
        self.view_count = self.channel["items"][0]["statistics"]['viewCount']
        # количество лайков
        self.like_count = int(self.channel['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, channel_id: str, id_playlist: str):
        self.id_playlist = id_playlist
        super().__init__(channel_id)