# import csv
import re
import requests
from bs4 import BeautifulSoup


RANDOM_LYRICS_URL = r'http://www.stixoi.info/stixoi.php?info=Lyrics&act=random'
LYRICS_FILENAME = 'lyrics.csv'
MAX_SONGS = 10000
SEP = '\t'


def clean_title(title):
    """
        Cleans the input `title` based on some rules

    :param title: Input title to clean
    :type title: str
    :return:
    """
    # remove all trailing and leading whitespace
    title = title.strip()
    # get rid of newlines
    title = title.replace('\r\n', ' ')
    # get rid of newlines and trailing spaces
    title = title.replace('\n', ' ')

    # get rid of multiple spaces
    title = re.sub(' +', ' ', title)

    return title


def clean_lyrics(lyrics):
    """
        Cleans the input `lyrics` based on some rules

    :param lyrics: Input lyrics to clean
    :type lyrics: str
    :return:
    """
    # remove all trailing and leading whitespace
    lyrics = lyrics.strip()
    # get rid of \r
    lyrics = lyrics.replace('\r\n', '\n')
    # get rid of multiple newlines and trailing spaces
    lyrics = re.sub(r'(\s)*\n(\s)*', '\n', lyrics)

    # get rid of multiple spaces
    lyrics = re.sub(' +', ' ', lyrics)

    return lyrics


def get_n_random_lyrics(n):
    """
        Gets a dictionary of `{title: lyrics}` for n random songs
    :param n:
    :type n: int
    :return: songs_dict
    """

    if (not isinstance(n, int)) or (n <= 0) or (n > MAX_SONGS):
        raise ValueError(f'n must be a positive integer 1 - {MAX_SONGS}')
    songs_dict = {}

    for _ in range(n):
        html_text = requests.get(RANDOM_LYRICS_URL).text

        if html_text:
            soup = BeautifulSoup(html_text, features='html.parser')
            divs = soup.find_all('div', class_='lyrics')
            lyr = divs[0].text
            if not lyr:
                print('Lyrics missing, continue with next song')
            lyr = clean_lyrics(lyr)

            title_divs = soup.find_all('td', class_='poemtitle0')
            title = title_divs[0].text
            if not title:
                print('Lyrics missing, continue with next song')
            title = clean_title(title)

            songs_dict[title] = lyr

    return songs_dict


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

    if append:
        mode = 'a'
    else:
        mode = 'w'

    lyrics_dict = get_n_random_lyrics(n)

    try:
        with open(filename, mode, encoding='utf-8') as f:

            # Write title
            line = f'title{SEP}lyrics\n'
            f.write(line)

            # Write contents
            for title, lyrics in lyrics_dict.items():
                line = f'{title}{SEP}{lyrics}\n'
                f.write(line)

    except IOError:
        print('I/O error')


if __name__ == '__main__':
    write_n_random_lyrics_to_file(n=100, append=False)
