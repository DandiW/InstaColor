def emoji_for_label(label):
	if label == "neutral":
		return u'neutral.svg'
	elif label == "sadness":
		return u'sadness.svg'
	elif label == "anger":
		return u'anger.svg'
	elif label == "happiness":
		return u'happiness.svg'
	elif label == "fear":
		return u'fear.svg'
	elif label == "disgust":
		return u'disgust.svg'
	elif label == "contempt":
		return u'contempt.svg'
	elif label == "surprise":
		return u'surprise.svg'
	return "Ahh, missing Emoji"

def emoji_for_label_byNumber(num):
	if num == "neu":
		return u'neutral_text.svg'
	elif num == "neg":
		return u'sadness_text.svg'
	elif num == "pos":
		return u'happiness_text.svg'
	return "Ahh, missing Emoji"
