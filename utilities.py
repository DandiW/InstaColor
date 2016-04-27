def emoji_for_label(label):
    if label == "neutral":
        return u'neutral.png'
    elif label == "sadness":
        return u'sadness.png'
    elif label == "anger":
        return u'anger.png'
    elif label == "happiness":
        return u'happiness.png'
    elif label == "fear":
        return u'fear.png'
    elif label == "disgust":
        return u'disgust.png'
    elif label == "contempt":
        return u'contempt.png'
    elif label == "surprise":
        return u'surprise.png'
    return "Ahh, missing Emoji"

def emoji_for_label_byNumber(num):
    if num == "neu":
        return u'neutral.png'
    elif num == "neg":
        return u'anger.png'
    elif num == "pos":
        return u'happiness.png'
    return "Ahh, missing Emoji"
