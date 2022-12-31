from bs4 import BeautifulSoup as b
import requests
import os

URL = "https://ruo.morsmusic.org/artist/"
url_site = "https://ruo.morsmusic.org"
id = "973"
pathToMusicFolder = "C:\\Users\\Sergey\\Desktop\\music\\"

def parse(url, block, _class):
    r = requests.get(url)
    print(r.status_code)
    soup = b(r.text, 'html.parser')
    content = soup.find_all(block, class_=_class)
    # clear_content = [c.text for c in content]
    return content


def downloadMusic():
    music_block = parse(URL + id, 'div', 'track mustoggler __adv_list_track')

    try:
        i = 2
        while i<= 4:
            music_block+=parse(URL + id+"?page="+str(i), 'div', 'track mustoggler __adv_list_track')
            i+=1
    except BaseException:
        print("empty")

    music_block.reverse()

    count = 0
    while count <= len(music_block):
        info = music_block[int(count) - 1]
        link = info.find('a', {"class": "track-download"}).get("href")
        name = info.find('a', {"class": "media-link media-name"}).text

        name.replace("\n", " ").strip()
        name =' '.join(name.split())

        artist = info.find('a', {"href": "/artist/"+id}).text
        duration = info.find('div', {"class": "track-duration-value track__fulltime"}).text
        duration = duration.replace(":","-")

        path = pathToMusicFolder

        if not os.path.isdir(path+artist+"\\"):
            os.mkdir(path+artist)

        path += artist+"\\"
        file_name = path + name+" "+duration+" "+artist+".mp3"
        print(file_name)
        try:
            data = requests.get(url_site+link)
            with open(file_name,'wb') as file:
                file.write(data.content)
            #urllib.request.urlretrieve(url_site+str(link),file_name)
        except BaseException:
            continue
        count += 1


if __name__ == "__main__":
    downloadMusic()