# flickrでスクレイピング

from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys
# APIキーの情報
key = "6b93e1130bb2a63feacb509d57f2fc53"
secret = "52c8f5444b7d2392"
wait_time = 1 #1秒おきにリクエスト
imgname = ["カレーライス", "牛丼", "ラーメン"]
filename = ['curry', 'gyudon', 'ramen']
for i in range(len(imgname)):
    savedir = "./data/" + filename[i]
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    flickr = FlickrAPI(key, secret, format='parsed-json')
    result = flickr.photos.search(
    text = imgname[i],
    per_page = 500,
    media = 'photos',
    sort = 'relevance',
    safe_search = 1,
    extras = 'url_q, licence'
    )
    photos = result['photos']
    for j, photo in enumerate(photos['photo']):
        url_q = photo['url_q']
        filepath = savedir + '/' + photo['id'] + '.jpg'
        if os.path.exists(filepath): continue
        urlretrieve(url_q,filepath)

    print(imgname[i] + " done")

print("all done")
