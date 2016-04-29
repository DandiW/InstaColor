from flask import *
import algorithms
import face
import instagram
import json
import operator
import os
import utilities

app = Flask(__name__)
app.debug = True

def save_access_token(access_token):
	assert(access_token is not None)
	data = {
		"access_token": access_token
	}
	with open('config.json', 'w') as file:
		json.dump(data, file)

def load_access_token():
	try:
		with open('config.json', 'r') as file:
			return json.load(file)["access_token"]
	except:
		# can't open the file, so we don't have a token
		return None

@app.route("/user")
def serve_user():
	if "code" in request.args:
		# get the access token, we just finished signing in
		code = request.args["code"]
		access_token = instagram.load_access_token(code)
		save_access_token(access_token)
	else:
		# ensure we already have an access token
		assert(load_access_token() is not None)
	
	return render_template('user.html')

@app.route("/stream/<user>")
def serve_stream(user):
	access_token = load_access_token()
	
	if access_token is None:
		return redirect("/", code=302)
	
	client = instagram.InstagramClient(access_token)
	photos = client.get_photos_for_user(user)
	top_filters = algorithms.find_top_filters(photos)
	top_emoji = algorithms.find_top_emoji(photos)

########################>>>TEST<<########################################
	#algorithms.sentiment_captions(photos)
	#algorithms.sentiment_captions2(photos)

####################>>>TEST-END<<########################################

	if "filter" in request.args:
		filter_name = request.args["filter"].lower()
		photos = algorithms.filter_photos_by_filter(photos, filter_name)
	elif "emoji" in request.args:
		emoji = request.args["emoji"]
		photos = algorithms.filter_photos_by_emoji(photos, emoji)
	
	userInfo = client.get_user_info()
	return render_template('stream.html', photos=photos, user=userInfo, top_filters=top_filters, top_emoji=top_emoji)

@app.route("/chart/<user>")
def serve_chart(user):
	access_token = load_access_token()
	
	if access_token is None:
		return redirect("/", code=302)
	
	client = instagram.InstagramClient(access_token)
	photos = client.get_photos_for_user(user)

	userInfo = client.get_user_info()
	return render_template('chart.html', photos=photos, user=userInfo)

@app.route("/photo/<id>")
def serve_photo(id):
	access_token = load_access_token()
	
	if access_token is None:
		return render_template('error.html', message="You are not signed in.")
	
	client = instagram.InstagramClient(access_token)
	photo = client.get_photo_info(id)
	
	return render_template('photo.html', photo=photo)

@app.route("/analyzeFaceSentiment")
def serve_face_sentiment():
	url = request.args["url"]
	ident = request.args["id"]
	assert(url is not None)
	
	access_token = load_access_token()
	
	if access_token is None:
		return render_template('error.html', message="You are not signed in.")
	
	client = instagram.InstagramClient(access_token)
	photo = client.get_photo_info(ident)
	
	label = face.analyze_image_at_url(url)

	emoji = "Unknown"

	if label is not None:
		emoji = utilities.emoji_for_label(label)
	else:
		dict_ = algorithms.sentiment_captions2(photo.caption)
		if dict_ is not None:
			if dict_["neg"] < 0.0001 and dict_["pos"] < 0.0001:
				label = "neu"
			else:
				label = max(dict_.iteritems(), key=operator.itemgetter(1))[0]
			emoji = utilities.emoji_for_label_byNumber(label)

	return json.dumps({
		#"label": utilities.emoji_for_label(label) if label is not None else "Unknown",
		"label": emoji,
		"raw_label": label if label is not None else "unknown",
		"identifier": ident
	})

@app.route("/analyzeColor")
def serve_analysis():
	url = request.args["url"]
	ident = request.args["id"]
	assert(url is not None)
	return json.dumps({
		"color": algorithms.find_primary_color(url),
		"identifier": ident
	})

@app.route("/signOut")
def serve_sign_out():
	os.remove("config.json")
	return redirect("/", code=302)

@app.route("/")
def serve_root():
	if load_access_token() is None:
		# sign in if we don't have an access token
		return render_template('index.html', auth_url=instagram.get_sign_in_url())
	else:
		# we're already signed in!
		# redirect to user chooser
		return redirect("/user", code=302)

if __name__ == "__main__":
	app.run(threaded=True)
