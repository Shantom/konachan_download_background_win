import ctypes
import os
import random
import urllib
import requests


class BackGroundSetter:
    def __init__(self, tags=[]):
        self.PicPath = os.path.join(os.path.expanduser("~"), 'Pictures')
        self.PicPath = os.path.join(self.PicPath, 'konachan')
        self.tags = tags
        self.firstTag = tags[0]
        self.finalPath = os.path.join(self.PicPath, self.firstTag)

    def start(self):
        images = os.listdir(self.finalPath)

        def isValid(name):
            name = os.path.splitext(name)[0]
            requiredTags = set(self.tags)
            imageTags = set(urllib.parse.unquote(name).split())
            # print(requiredTags)
            # print(imageTags)
            return requiredTags.issubset(imageTags)

        images = list(filter(isValid, images))
        if len(images) == 0:
            print('No valid image.')
            return
        image = random.choice(images)
        print('Image set. '+image)
        imagePath = os.path.join(self.finalPath, image)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 0)


if __name__ == '__main__':
    tags = ['fjsmu']
    setter = BackGroundSetter(tags)
    setter.start()
