# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from os.path import expanduser
from functools import partial
import time

from SimpleCV import Camera, Image, Color, DrawingLayer, Kinect, Display

import numpy as np


def find_corners(b, color=Color.ORANGE, erode=3, circlet=.3, radius=10):
    #c = b.colorDistance(color)
    c = b.hueDistance(color)

    balls = (b-c).erode(erode)
    #balls = c.binarize(70).morphClose()
    balls.show()

    binBlobs = balls.findBlobs(minsize=radius)
    corners = binBlobs.filter([blob.isCircle(circlet) for blob in binBlobs])
    binBlobs.show()
    raw_input()
    corners.show()

    return corners

def find_boat(b, color=Color.CRIMSON, erode=3, circlet=.3, radius=10):
    c = b.hueDistance(color)

    balls = (b-c)#.erode(erode)
    
    binBlobs = balls.findBlobs(maxsize=radius)
    binBlobs.show()
    
    boat = binBlobs.filter([blob.isCircle(circlet) for blob in binBlobs])
    binBlobs.show()
    
    print "boats", boat
    return boat.sortArea()[0]


def distance(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    return np.math.sqrt((x1-x2)**2 + (y1-y2)**2)

def topLeft(corners):
    dists = map(partial(distance, (0,0)), corners)
    return corners[np.argmin(dists)]

def bottomRight(corners):
    dists = map(partial(distance, (0,0)), corners)
    return corners[np.argmax(dists)]

def clockwise_corners(corners, img):
    dists_origin = map(partial(distance, (0,0)), corners)
    dists_tr = map(partial(distance, (img.width, 0)), corners)
    return (corners[np.argmin(dists_origin)], 
            corners[np.argmin(dists_tr)], 
            corners[np.argmax(dists_origin)],
            corners[np.argmax(dists_tr)])

def draw_blobs(img, corners, boat):
    centers = [blob.centroid() for blob in corners]
    tl = topLeft(centers)
    br = bottomRight(centers)
    maplayer = DrawingLayer((img.width, img.height))
    maplayer.rectangle(tl, (br[0]-tl[0], br[1]-tl[1]))

    for blob in corners:
        maplayer.circle(blob.centroid(), radius=20)
    maplayer.circle(boat.centroid(), radius=10)

    pos = boat_lat_lon(boat, corners)
    maplayer.text("(%.2f, %.2f)" % (pos[0], pos[1]), boat.centroid(), color=Color.WHITE)
    
    img.addDrawingLayer(maplayer)
    img.applyLayers()
    img.show()
    
def boat_lat_lon(boat, corners):
    centers = [blob.centroid() for blob in corners]
    bcenter = boat.centroid()
    
    tl = topLeft(centers)
    br = bottomRight(centers)
    
    total_lats = br[1] - tl[1]
    total_lons = br[0] - tl[0]
    
    boat_lats = bcenter[1] - tl[1]
    boat_lons = bcenter[0] - tl[0]
    
    lon = float(boat_lons)/total_lons * 360. - 180
    lat = 90 - float(boat_lats)/total_lats * 180.
    
    return lat, lon

# <codecell>

def get_image():
    a = Camera(0)
    #a = Kinect()
    time.sleep(1)
    b = a.getImage()
    #b.save(expanduser("~/Projects/OceanColorSound/frame4.png"))
    #b = Image(expanduser("~/Projects/OceanSound/data/frame4.png"))
    return b

def calibrate():
    winsize = (640,480)
    display = Display(winsize)
    bg_img = get_image()
    bg_img.save(display)
    while not display.isDone():
        img = get_image()
        img.save(display)
        if display.mouseLeft:
            return img.getPixel(display.mouseX, display.mouseY), bg_img, img

def process():
#    try:
    b = get_image()
    corners = find_corners(b, Color.ORANGE, circlet=.4)
    boat = find_boat(b, Color.ORANGE, corners, circlet=.3, erode=1, radius=8)
    draw_blobs(b, corners, boat)
#    except:
#        pass
    #b.save(expanduser("~/Projects/OceanColorSound/resultado.png"))
    
def process2():
    a = Camera()
    b = a.getImage()
    #b.save(expanduser("~/Projects/OceanColorSound/frame4.png"))
    #b = Image(expanduser("~/Projects/OceanColorSound/frame4.png"))
    b.show()

    corners = find_corners(b, Color.ORANGE, circlet=.4)
    print "shear"
    tl, tr, br, bl = clockwise_corners([blob.centroid() for blob in corners], b)
#    fixed = b.shear([(0,0), (b.width, tl[1]-tr[1]), (b.width, b.height), (0, b.height)])
#    fixed = b.shear([tl, (br[0], tl[1]), br, (tl[1], br[1])])
    fixed = b.warp([tl, (br[0], tl[1]), br, (tl[0], br[1])])
    fixed.show()
    print "shear"
    new_corners = find_corners(fixed, Color.ORANGE, circlet=.4, radius=10)
    print new_corners
    #boat = find_boat(fixed, Color.ORANGE, new_corners, circlet=.3, erode=1, radius=10)
    #draw_blobs(b, corners, boat)
    draw_blobs(fixed, new_corners, new_corners[0])

# <codecell>

#while True:
#    process()
#    time.sleep(5)
#process()
