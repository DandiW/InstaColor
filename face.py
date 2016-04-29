# Microsoft api - Facial emotion anaysis

import json
import operator
import requests
import time

RECOGNIZE_URL = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
KEY = '981cde578f8540b1957f8908b87c6c09'
MAX_NUM_RETRIES = 10

def analyze_image_at_url(image_url):
	headers = {}
	headers['Ocp-Apim-Subscription-Key'] = KEY
	headers['Content-Type'] = 'application/json'
	
	json_input = { 'url': image_url }
	data = json.dumps(json_input)
	
	for retry in range(MAX_NUM_RETRIES):
		response = requests.request('post', RECOGNIZE_URL, json=json, data=data, headers=headers, params=None)
		
		# 429 = too many requests, try again after 1 sec
		if response.status_code == 429: 
			print("429 Message: %s" % response.json()['error']['message'])
			time.sleep(1)
			continue
		elif response.status_code == 200 or response.status_code == 201:
			if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
				return None
			elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
				if 'application/json' in response.headers['content-type'].lower():
					faces = response.json() if response.content else None
					return extract_most_probable_label(faces)
				elif 'image' in response.headers['content-type'].lower():
					# when would this give back an image
					assert(False)
		else:
			print("Error code: %d" % response.status_code)
			print("Message: %s" % response.json()['error']['message'])
	
	print("Error: we tried %d times but the requests still failed" % MAX_NUM_RETRIES)
	return None

def extract_most_probable_label(faces):
	for face in faces:
		best_label = max(face['scores'].iteritems(), key=operator.itemgetter(1))[0]
		return best_label
		#TODO: this only considers the first face 
