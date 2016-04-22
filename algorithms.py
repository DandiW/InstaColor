from sklearn.cluster import KMeans
import operator
import requests
import numpy
from StringIO import StringIO
from PIL import Image

def find_primary_color(url):
    request = requests.get(url)
    img = Image.open(StringIO(request.content))
    matrix = numpy.asarray(img)
    pixel_count = matrix.shape[0] * matrix.shape[1]
    pixels = matrix.reshape(pixel_count, 3, 1).squeeze()
    assert(pixels.shape[1] == 3)
    
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(pixels)
    assert(kmeans.cluster_centers_.shape[0] == 1)
    top_pixel = kmeans.cluster_centers_[0,:]
    
    color = "rgb(" + str(int(top_pixel[0])) + "," + str(int(top_pixel[1])) + "," + str(int(top_pixel[2])) + ")"
    return color

def filter_photos_by_filter(photos, filter_name):
    passing_photos = []
    for photo in photos:
        if filter_name in photo.filter.lower():
            passing_photos.append(photo)
    return passing_photos

def filter_photos_by_emoji(photos, emoji):
    passing_photos = []
    for photo in photos:
        if photo.caption is not None and emoji in photo.caption:
            passing_photos.append(photo)
    return passing_photos

class Filter:
    def __init__(self, name):
        self.name = name

class Emoji:
    def __init__(self, content):
        self.content = content

def find_top_filters(photos):
    filter_map = {}
    for photo in photos:
        filter_key = photo.filter.lower()
        if filter_key in filter_map:
            filter_map[filter_key] += 1
        else:
            filter_map[filter_key] = 1
    sorted_items = sorted(filter_map.items(), key=operator.itemgetter(1))
    filters = []
    for key, value in sorted_items:
        filters.append(Filter(key))
    return filters

# Emojis are stored as a surrogate pairs
def is_surrogate(string, i):
    if i+1 >= len(string):
        return False
    
    if 0xD800 <= ord(string[i]) <= 0xDBFF:
        l = string[i+1]
        if 0xDC00 <= ord(l) <= 0xDFFF:
            return True
        else:
            raise ValueError("Illegal UTF-16 sequence: %r" % string[i:i+2])
    else:
        return False

def emoji_in_photo(photo): 
    if photo.caption is None:
        return []
    
    all_emoji = []
    for i in range(len(photo.caption)):
        if is_surrogate(photo.caption, i):
            all_emoji.append(photo.caption[i:i+2])
    return all_emoji

def find_top_emoji(photos):
    filter_map = {}
    for photo in photos:
        for emoji in emoji_in_photo(photo):
            if emoji in filter_map:
                filter_map[emoji] += 1
            else:
                filter_map[emoji] = 1
    sorted_items = sorted(filter_map.items(), key=operator.itemgetter(1))
    emojis = []
    for key, value in sorted_items:
        emojis.append(Emoji(key))
    return emojis
