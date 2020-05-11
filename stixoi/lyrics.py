from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


RANDOM_LYRICS_URL = r'http://www.stixoi.info/stixoi.php?info=Lyrics&act=random'
LYRICS_FILENAME = 'lyrics.txt'

SLEEP_TIME = 30


@dataclass
class Site:
    url: str


def clean_lyrics(lyrics):
    """
        Cleans the input `lyrics` based on some rules

    :param lyrics: Input lyrics to clean
    :type lyrics: str
    :return:
    """
    # split / remove all whitespace
    lyrics = lyrics.strip()
    lyrics = lyrics.replace('\r\n', '\n')
    lyrics = lyrics.replace('\n\n', '\n')
    lyrics_list = lyrics.split('\n')
    # strip empty space
    lyrics_list = [s.strip() for s in lyrics_list if s]
    # join by tab
    lyrics = '\t'.join(lyrics_list)
    return lyrics


def yield_n_random_lyrics(n):
    """
        Gets a list of lyrics for n random songs
    :param n:
    :type n: int
    :return: lyrics_list
    """

    assert isinstance(n, int)
    assert n > 0

    for _ in range(n):
        html_text = requests.get(RANDOM_LYRICS_URL).text

        if html_text:
            soup = BeautifulSoup(html_text, features='html.parser')
            divs = soup.find_all('div', class_='lyrics')
            assert divs
            lyr = divs[0].text
            assert lyr
            lyr = clean_lyrics(lyr)

            yield lyr


def write_n_random_lyrics_to_file(n, filename=LYRICS_FILENAME,
                                  append=False, compress=False):
    """
        Downloads `n` random songs to a filename, separated by new line

    :param n:
    :param filename:
    :param append:
    :param compress
    :return:
    """

    if compress:
        raise NotImplementedError(
            'Compression not enabled yet')

    if not append:
        mode = 'w'
    else:
        mode = 'a'

    for lyr in yield_n_random_lyrics(n):
        with open(filename, mode, encoding='utf-8') as f:
            f.writelines(lyr + '\n')

        # continue appending
        mode = 'a'


if __name__ == '__main__':
    num_lyrics_to_download = 5
    write_n_random_lyrics_to_file(
        num_lyrics_to_download, append=True)
