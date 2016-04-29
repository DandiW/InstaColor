import tokenize
import pprint

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from sklearn.cluster import KMeans
import operator
import requests
import numpy
import colorsys
from StringIO import StringIO
from PIL import Image
from textblob import TextBlob


def find_primary_color(url):
	request = requests.get(url)
	img = Image.open(StringIO(request.content))
	matrix = numpy.asarray(img)
	pixel_count = matrix.shape[0] * matrix.shape[1]
	pixels = matrix.reshape(pixel_count, 3, 1).squeeze()
	assert (pixels.shape[1] == 3)

	# find the top K color clusters but only uses the most frequent one
	# by treating K-1 clusters as a junk drawer, the color accuracy of the primary cluster is improved
	key_clusters = 3
	junk_clusters = 2
	kmeans = KMeans(n_clusters=junk_clusters + key_clusters)
	kmeans.fit(pixels)
	assert (kmeans.cluster_centers_.shape[0] == junk_clusters + key_clusters)
	cluster_counts = {}
	for i in range(junk_clusters + key_clusters):
		cluster_counts[i] = 0

	for i in kmeans.labels_:
		cluster_counts[i] += 1

	sorted_items = sorted(cluster_counts.items(), key=operator.itemgetter(1), reverse=True)

	top_pixels = []
	for i in range(key_clusters):
		color = kmeans.cluster_centers_[sorted_items[i][0], :]
		hsv = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
		top_pixels.append((color, hsv))

	sorted_colors = sorted(top_pixels, key=lambda x: x[1][1])
	best_color = sorted_colors[1]
	best_color_rgb = best_color[0]
	color = "rgb(" + str(int(best_color_rgb[0])) + "," + str(int(best_color_rgb[1])) + "," + str(
		int(best_color_rgb[2])) + ")"
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
	sorted_items = sorted(filter_map.items(), key=operator.itemgetter(1), reverse=True)
	filters = []
	for key, value in sorted_items:
		filters.append(Filter(key))
	return filters


# Emojis are stored as a surrogate pairs
def is_surrogate(string, i):
	if i + 1 >= len(string):
		return False

	if 0xD800 <= ord(string[i]) <= 0xDBFF:
		l = string[i + 1]
		if 0xDC00 <= ord(l) <= 0xDFFF:
			return True
		else:
			raise ValueError("Illegal UTF-16 sequence: %r" % string[i:i + 2])
	else:
		return False


def emoji_in_photo(photo):
	if photo.caption is None:
		return []

	all_emoji = []
	for i in range(len(photo.caption)):
		if is_surrogate(photo.caption, i):
			all_emoji.append(photo.caption[i:i + 2])
	return all_emoji


def find_top_emoji(photos):
	filter_map = {}
	for photo in photos:
		for emoji in emoji_in_photo(photo):
			if emoji in filter_map:
				filter_map[emoji] += 1
			else:
				filter_map[emoji] = 1
	sorted_items = sorted(filter_map.items(), key=operator.itemgetter(1), reverse=True)
	emojis = []
	for key, value in sorted_items:
		emojis.append(Emoji(key))
	return emojis


# entiment analysis on captions and tags
def sentiment_captions(photos):
	polar = {}
	for photo in photos:
		if photo.caption is None:
			continue

		caption_without_emoji = photo.caption.encode('ascii', 'ignore')
		text = TextBlob(caption_without_emoji)
		# store the polarity
		# Note 0 = neutral. greater than 0 means happy/good/postive. Less than 0 = sad/negative
		polar[photo.identifier] = text.sentiment.polarity

		# print text.sentiment

	return polar


def sentiment_captions2(caption):
	if caption is None:
		return None
	temp = {}
	caption_without_emoji = caption.encode('ascii', 'ignore')
	lines_list = tokenize.sent_tokenize(caption_without_emoji)
	sid = SentimentIntensityAnalyzer()
	for sentence in lines_list:
		ss = sid.polarity_scores(sentence)
		for k in sorted(ss):
			if k == "compound" or k == "neu":
				continue
			if k in temp:
				temp[k] += ss[k]
			else:
				temp[k] = ss[k]
	return temp
	# print polar
	'''
		polar format:
		polar[photo.id] = {
							neg : 0.0
							neu : 0.0
							pos : 0.0
							compound: 0.0
						   }
	'''
