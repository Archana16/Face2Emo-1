#!/usr/bin/python

"""
Save this file as server.py
>>> python server.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python server.py
Serving on localhost:8000

You can use this to test GET and POST methods.

"""

import SimpleHTTPServer
import SocketServer
import logging
import cgi
import cv
import cv2
import time
from PIL import Image
import numpy as np
import csv
import logistic
import mouthdetection as m

import sys

WIDTH, HEIGHT = 28, 10 # all mouth images will be resized to the same size
dim = WIDTH * HEIGHT # dimension of feature vector

"""
pop up an image showing the mouth with a blue rectangle
"""
def show(area): 
    cv.Rectangle(img,(area[0][0],area[0][1]),
                     (area[0][0]+area[0][2],area[0][1]+area[0][3]),
                    (255,0,0),2)
    cv.NamedWindow('Face Detection', cv.CV_WINDOW_NORMAL)
    cv.ShowImage('Face Detection', img) 
    cv.WaitKey()

"""
given an area to be cropped, crop() returns a cropped image
"""
def crop(area, img): 
    crop = img[area[0][1]:area[0][1] + area[0][3], area[0][0]:area[0][0]+area[0][2]] #img[y: y + h, x: x + w]
    return crop

"""
given a jpg image, vectorize the grayscale pixels to 
a (width * height, 1) np array
it is used to preprocess the data and transform it to feature space
"""
def vectorize(filename):
    size = WIDTH, HEIGHT # (width, height)
    im = Image.open(filename) 
    resized_im = im.resize(size, Image.ANTIALIAS) # resize image
    im_grey = resized_im.convert('L') # convert the image to *greyscale*
    im_array = np.array(im_grey) # convert to np array
    oned_array = im_array.reshape(1, size[0] * size[1])
    return oned_array


if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""

"""
    load training data
    """
# create a list for filenames of smiles pictures
smilefiles = []
with open('smiles.csv', 'rb') as csvfile:
	for rec in csv.reader(csvfile, delimiter='	'):
		smilefiles += rec

# create a list for filenames of neutral pictures
neutralfiles = []
with open('neutral.csv', 'rb') as csvfile:
	for rec in csv.reader(csvfile, delimiter='	'):
		neutralfiles += rec

# N x dim matrix to store the vectorized data (aka feature space)       
phi = np.zeros((len(smilefiles) + len(neutralfiles), dim))
# 1 x N vector to store binary labels of the data: 1 for smile and 0 for neutral
labels = []

# load smile data
PATH = "../data/smile/"
for idx, filename in enumerate(smilefiles):
	phi[idx] = vectorize(PATH + filename)
        labels.append(1)

# load neutral data    
PATH = "../data/neutral/"
offset = idx + 1
for idx, filename in enumerate(neutralfiles):
	phi[idx + offset] = vectorize(PATH + filename)
        labels.append(0)

"""
training the data with logistic regression
"""
lr = logistic.Logistic(dim)
lr.train(phi, labels)
    


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        logging.warning("======= POST VALUES =======")
	image_base64 = form.getvalue("image")
	g = open("out.jpg", "w")
	g.write(image_base64.decode('base64'))
	g.close()
        img = cv.LoadImage("out.jpg") # input image
        mouth = m.findmouth(img)
        # show(mouth)
        if mouth != 2: # did not return error
        	mouthimg = crop(mouth, img)
                cv.SaveImage("webcam-m.jpg", mouthimg)
                # predict the captured emotion
                result = lr.predict(vectorize('webcam-m.jpg'))
                if result == 1:
                    print "you are smiling! :-) "
		    ans = "S"
                else:
                    print "you are not smiling :-| "
		    ans = "F"
	else:
		ans = "D"
                print "failed to detect mouth. Try hold your head straight and make sure there is only one face."
        logging.warning("\n")
	self.send_response(200, "OK")
	self.send_header("Content-type", "application/json")
	self.end_headers()
	print ans
	self.wfile.write("{result:" + ans + "}")
	#self.wfile.close()
        #SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "@rochacbruno Python http server version 0.1 (for testing purposes only)"
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()
