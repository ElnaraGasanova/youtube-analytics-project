import os
import datetime
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('API_KEY')
    '''Создан класс для получения информации о плейлисте'''
    def __init__(self, playlist_id: str) -> None:
        '''Экземпляр инициализируется по id плейлиста.
        Дальше все данные будут подтягиваться по API.'''
        self.playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id


    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)


    def get_playlist_title(self):
        '''Функция получения названия плейлиста'''
        channel_id = self.get_playlist_data()["items"][0]["snippet"]["channelId"]
        channel_playlists_data = self.get_service().playlists().list(channelId=channel_id,
                                                                        part='contentDetails,snippet',
                                                                        maxResults=50,
                                                                        ).execute()
        for playlist in channel_playlists_data["items"]:
            if self.playlist_id == playlist["id"]:
                playlist_title = playlist["snippet"]["title"]
                return playlist_title

    def get_playlist_data(self):
        '''Функция получения данных плейлиста'''
        youtube = self.get_service()
        playlist_data = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                     part='contentDetails, id, snippet, status',
                                                     maxResults=50,
                                                     ).execute()
        return playlist_data

    def get_videos_id(self):
        '''Функция получения списка id видео в плейлисте'''
        videos = self.get_playlist_data()
        videos_id = []

        for video in videos['items']:
            videos_id.append(video['contentDetails']['videoId'])

        return videos_id

    def get_videos_from_playlist(self):
        '''Функция получения данных о видео в плейлисте'''
        videos_id = self.get_videos_id()
        youtube = self.get_service()
        videos_in_playlist = youtube.videos().list(part='contentDetails,statistics',
                                                   id=','.join(videos_id)
                                                   ).execute()
        return videos_in_playlist

    def get_videos_duration(self):
        '''Функция получения длины каждого видео из плейлиста'''
        videos_duration = self.get_videos_from_playlist()["items"]
        video_duration_list = []
        for video in videos_duration:
            iso_8601_duration = video['contentDetails']['duration']
            video_duration_list.append(isodate.parse_duration(iso_8601_duration))
        return video_duration_list

    @property
    def total_duration(self):
        '''Функция получения общей длины всех видео в плейлисте'''
        total_duration = sum(self.get_videos_duration(), datetime.timedelta())
        return total_duration

    def show_best_video(self):
        '''Функция получения ссылки на видео
        с бОльшим кол-вом лайков в плейлисте'''
        playlist_videos = self.get_videos_from_playlist()
        most_liked_video = 0

        for video in playlist_videos["items"]:
            if most_liked_video < int(video["statistics"]["likeCount"]):
                most_liked_video = int(video["statistics"]["likeCount"])
                most_liked_video_id = video["id"]

        return f"https://youtu.be/{most_liked_video_id}"
