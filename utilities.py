def emoji_for_label(label):
    if label == "neutral":
        return u'\U0001f610'
    elif label == "sadness":
        return u'\U0001f622'
    elif label == "anger":
        return u'\U0001f621'
    elif label == "happiness":
        return u'\U0001f600'
    elif label == "fear":
        return u'\U0001f628'
    elif label == "disgust":
        return u'\U0001f637'
    elif label == "contempt":
        return u'\U0001f644'
    elif label == "surprise":
        return u'\U0001f62f'
    return "Ahh, missing Emoji"

def emoji_for_label_byNumber(num):
    if num == "neu":
        return u'\U0001f610'
    elif num == "neg":
        return u'\U0001f621'
    elif num == "pos":
        return u'\U0001f600'
    return "Ahh, missing Emoji"
