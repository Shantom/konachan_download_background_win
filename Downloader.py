import os
import requests
import json
import time


class Downloader:
    def __init__(self, tags=[], limit=5):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        }
        self.proxies = {
            'http': 'socks5://127.0.0.1:1080',
            'https': 'socks5://127.0.0.1:1080'
        }
        self.PicPath = os.path.join(os.path.expanduser("~"), 'Pictures')
        self.PicPath = os.path.join(self.PicPath, 'konachan')

        self.params = {'tags': None,
                       'limit': limit
                       }
        self.setTags(tags)

        os.makedirs(self.finalPath, exist_ok=True)

        self.url_net = 'https://konachan.net/post.json'

    def setTags(self, tags):
        self.tags = ' '.join(tags)
        self.firstTag = tags[0]
        self.finalPath = os.path.join(self.PicPath, self.firstTag)
        self.params['tags'] = self.tags

    def setLimit(self, limit):
        self.params['limit'] = limit

    def start(self):
        if len(self.tags) == 0:
            print('No tags.')
            return

        print(self.params)
        req = requests.get(self.url_net, headers=self.headers,
                           proxies=self.proxies, params=self.params).content
        jsonList = json.loads(req)
        if len(jsonList) == 0:
            print('No such tags.')

        for item in jsonList:
            idNo = str(item['id'])
            if item['rating'] not in ['s', 'safe']:
                print('This image is not good. ' + idNo)
                continue

            file_url = item['file_url']
            file_name = file_url.split(
                '/')[-1].replace('%20', ' ').replace('Konachan.com - ', '')

            file_dir = os.path.join(self.finalPath, file_name)

            if os.access(file_dir, os.F_OK):
                print('This image is already here.' + idNo)
                continue

            try:
                image = requests.get(file_url, headers=self.headers,
                                     proxies=self.proxies).content
                with open(file_dir, 'wb') as f:
                    print('Downloading image. ' + idNo)
                    f.write(image)
            except:
                print('Download failed. ' + idNo)


if __name__ == '__main__':
    tags = ['fjsmu']
    tags = input().split()
    DL = Downloader(tags, 50)
    DL.start()
