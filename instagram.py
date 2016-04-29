import json
import requests
import urllib
import datetime
from pytz import timezone

CLIENT_ID="efd747770079428c812e17391edc8e87"
CLIENT_SECRET="72b3719a0f994d7d9a360510a9d18199"
REDIRECT="http://localhost:5000/user"
ENCODED_REDIRECT="http%3A%2F%2Flocalhost%3A5000%2Fuser"

class Photo:
	def __init__(self, identifier, thumbnail_url, standard_resolution_url, filter_name, caption, location, creation_date, likes):
		self.identifier = identifier
		self.thumbnail_url = thumbnail_url
		self.standard_resolution_url = standard_resolution_url
		self.filter = filter_name
		self.caption = caption
		self.location = location
		self.creation_date = creation_date
		self.likes = likes

class User:
	def __init__(self, name, profile_picture_link):
		self.name = name
		self.profile_picture_link = profile_picture_link

class InstagramClient:
	def __init__(self, token):
		self.access_token = token
	
	def photo_from_data(self, data):
		thumbnail_url = data["images"]["thumbnail"]["url"]
		standard_res_url = data["images"]["standard_resolution"]["url"]
		filter_name = data["filter"]
		identifier = data["id"]
		caption = data["caption"]["text"] if data["caption"] is not None else None
		location = data["location"]["name"] if data["location"] is not None else None
		ts = int(data["created_time"])
		local_tz = timezone("America/Chicago")
		creation_date = local_tz.localize(datetime.datetime.fromtimestamp(ts))
		likes = int(data["likes"]["count"])
		return Photo(identifier, thumbnail_url, standard_res_url, filter_name, caption, location, creation_date, likes)
	
	def user_from_data(self, data):
		return User(data["full_name"], data["profile_picture"])
	
	def get_photos_for_user(self, user):
		url = "https://api.instagram.com/v1/users/" + user + "/media/recent?access_token=" + urllib.quote(self.access_token, safe='')
		request = requests.get(url)
		response = request.json()
		if response is None:
			return []
		all_photos = []
		for entry in response["data"]:
			all_photos.append(self.photo_from_data(entry))
		return all_photos
	
	def get_photo_info(self, id):
		url = "https://api.instagram.com/v1/media/" + id + "?access_token=" + urllib.quote(self.access_token, safe='')
		request = requests.get(url)
		response = request.json()
		if response is None:
			return []
		entry = response["data"]
		return self.photo_from_data(entry)
	
	def get_user_info(self):
		url = "https://api.instagram.com/v1/users/self?access_token=" + urllib.quote(self.access_token, safe='')
		request = requests.get(url)
		response = request.json()
		if response is None:
			return []
		entry = response["data"]
		return self.user_from_data(entry)

def load_access_token(code):
	request = requests.post('https://api.instagram.com/oauth/access_token', data={
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'grant_type': "authorization_code",
		'redirect_uri': REDIRECT,
		'code': code
	})
	response = request.json()
	if response is None:
		return None
	return response["access_token"]

def get_sign_in_url():
	return "https://api.instagram.com/oauth/authorize/?client_id=" + CLIENT_ID + "&redirect_uri=" + ENCODED_REDIRECT + "&response_type=code"
