import json

import requests



# Microsoft api - Facial emotion anaysis

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = '981cde578f8540b1957f8908b87c6c09' #Here you have to paste your primary key
_max_num_retries = 10

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json' 

json = { 'url': urlImage } 
data = None

result = processRequest( json, data, headers )

urlImage = get_urlImage(self, id)


class scores:
    def get_max_score(photo):
        for currFace in photo:
            currEmotion = max(currFace['scores'].iteritems(), key=operator.itemgetter(1))[0]

    
class url:
    def get_urlImage(self, id)
        return "https://api.instagram.com/v1/media/" + id + "?access_token=" + urllib.quote(self.access_token, safe='')

class emotion:
    def get_face_info(self, id, photo)
        url = get_urlImage(self, id)
        request = requests.get(url)
        response = request.json()
        if response is None:
            return []
        entry = response["data"]
        return self.get_max_score(entry)
        
    
    
def processRequest( json, data, headers ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = None )

        if response.status_code == 429: 

            print "Message: %s" % ( response.json()['error']['message'] )

            if retries <= _max_num_retries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print 'Error: failed after retrying!'
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print "Error code: %d" % ( response.status_code )
            print "Message: %s" % ( response.json()['error']['message'] )

        break
        
    return result







