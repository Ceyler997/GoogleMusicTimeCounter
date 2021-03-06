'''File for library handler class'''
from datetime import timedelta
import json


class LibHandler:
    '''Class to work with music library'''

    def __init__(self, songs, out_file_path):
        self.uploaded_songs = list(map(self.convert_song, songs))
        self.uploaded_songs.sort(key=lambda song: song['album'])
        self.out_file_path = out_file_path

    def update_lib_file(self):
        '''Updates file with songs library'''
        with open(self.out_file_path + '.txt', 'w') as out_txt:
            for song in self.uploaded_songs:
                out_txt.write(f"'{song['title']}' FROM '{song['album']}' BY '{song['artist']}'\n")

        with open(self.out_file_path, 'w') as out_file:
            json.dump(self.uploaded_songs, out_file)

    @staticmethod
    def convert_song(song_info):
        '''Converts songs info from API to the internal format'''
        return {
            'id': song_info['id'],
            'title': song_info['title'],
            'album': song_info['album'],
            'artist': song_info['artist']
        }

class LibraryHandler:
    '''Class to work with music library'''

    library = list()

    def __init__(self, library):
        # todo: sort library by something
        self.library = library

    def __bool__(self):
        return bool(self.library)

    def update_lib_file(self, file_path):
        '''
        Writes all library to the passed file in a format:
        artist  album   title
        '''
        # todo: write a file creation (with path)
        # todo: Write a json instead of plain text
        with open(file_path, 'w', encoding='utf-8') as file:
            print('Updating library file')
            for song in self.library:
                file.write(song['artist'])
                file.write('\t')
                file.write(song['album'])
                file.write('\t')
                file.write(song['title'])
                file.write('\n')

    def get_playing_time(self) -> timedelta:
        '''Returns how much time spent to play music from library'''
        duration = timedelta()
        for song in self.library:
            if 'playCount' in song and 'durationMillis' in song:
                song_duration = int(song['durationMillis']) * song['playCount']
                duration = duration + timedelta(milliseconds=song_duration)

        return duration

    def get_genre_songs_statistic(self) -> [dict, int]:
        '''
        Returns genre library statistic in form of dictionary
        <genre, amount_of_songs> and total amount of songs
        '''
        # todo: sort by popularity
        lib_stat = dict()
        total = len(self.library)

        for song in self.library:
            song_genre = 'no genre'
            # Checks key exsistance and length
            if 'genre' in song and song['genre']:
                song_genre = song['genre']
            if song_genre in lib_stat:
                lib_stat[song_genre] = lib_stat[song_genre] + 1
            else:
                lib_stat[song_genre] = 1

        return lib_stat, total
