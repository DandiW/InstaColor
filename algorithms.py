from sklearn.cluster import KMeans
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
