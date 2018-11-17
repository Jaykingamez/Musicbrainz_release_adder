import requests
from bs4 import BeautifulSoup
from itertools import count
from datetime import datetime


def get_soup(url):
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
               }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return BeautifulSoup(r.text, 'lxml')


def album_title(soup):
    attrs = {'class': 'a-size-large a-spacing-micro'}
    return soup.find('h1', attrs=attrs).text


def album_type(tracks):
    if len(tracks) <= 2:
        return 'Single'
    elif len(tracks) <= 6:
        return 'EP'
    else:
        return 'Album'


def release_date(soup):
    attrs = {'class': 'a-size-base a-color-secondary'}
    date = soup.find('span', attrs=attrs).text.strip()
    return datetime.strptime(date, '%B %d, %Y').date()


def track_titles(soup):
    attrs = {'class': 'a-link-normal a-color-base TitleLink a-text-bold'}
    return [a.text for a in soup.find_all('a', attrs=attrs)[::2]]


def track_durations(soup):
    attrs = {'class': 'a-text-right a-align-center'}
    return [td.text.strip() for td in soup.find_all('td', attrs=attrs)]


def track_artist(soup):
    return soup.find('a', attrs={'id':'ProductInfoArtistLink'}).text


def track_multi_artist(soup):
    attrs = {'class':'a-link-normal a-color-base a-size-mini ArtistLink'}
    return [a2.text for a2 in soup.find_all('a', attrs=attrs)[::2]]


def track_label(soup, artis):
    inside_div = soup.find('div', attrs={'class': 'content'})
    inside_li = inside_div.find_all('li')[2]
    label = inside_li.find(text=True, recursive=False).strip()
    if label == artis:
        return '[no label]'
    return label


url = input("Please enter an Amazon music url:").strip()
soup = get_soup(url)
album = album_title(soup)
primary_type = album_type(track_titles(soup))
release_date = release_date(soup)
titles = track_titles(soup)
durations = track_durations(soup)
artis = track_artist(soup)
label = track_label(soup, artis)
multi_artist = track_multi_artist(soup)


if __name__ == "__main__":
    url = input("Please enter an Amazon music url:").strip()
    soup = get_soup(url)
    titles = track_titles(soup)
    durations = track_durations(soup)
    artist = track_artist(soup)
    multi_artist = track_multi_artist(soup)

    if len(multi_artist)== 0:
        for i, title, duration in zip(count(1), titles, durations):
            print(f"{i}. {title} - {artist} ({duration})")
    else:
        for i, title, duration, artist in zip(count(1), titles, durations, multi_artist):
            print(f"{i}. {title} - {artist} ({duration})")
