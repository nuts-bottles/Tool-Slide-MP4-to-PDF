import cv2
import os
from PIL import Image
import glob
from PIL import ImageFile
from numpy import average, dot, linalg

MP4_INPUT_NAME = "20200814.mp4"
CUTTED_GRAPH_FROM_FRAME = (0, 80, 1530, 1000)
CUTTED_GRAPH_PER_FRAME = 1000
FAMILIAR_FRAME_WINDOW = (250, 150)
FAMILIAR_FRAME_PERCENTAGE = 0.99

def get_glance(im):
     image =im.resize(FAMILIAR_FRAME_WINDOW)
     return image 

def image_similarity_vectors_via_numpy(image1, image2):
    image1 = get_glance(image1)
    image2 = get_glance(image2)
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    res = dot(a / a_norm, b / b_norm)
    return res

ImageFile.LOAD_TRUNCATED_IMAGES = True
 
path = './output/'
if not os.path.exists(path):
    os.mkdir(path)

vc = cv2.VideoCapture('./' + MP4_INPUT_NAME)
x = 0   # Saved jpg file
c = 0   # Temporatory file
t = CUTTED_GRAPH_PER_FRAME
rval = vc.isOpened()
while rval:
    rval, frame = vc.read()
    if (c % t == 1):
        cv2.imwrite(path + str(c) + '.jpg', frame)
        im = Image.open(path + str(c) + '.jpg') 
        im = im.crop(CUTTED_GRAPH_FROM_FRAME)
        if c == 1:
            ex_im = im
            im.save(path + str(x) + '.jpg')
            print("RECORD: " + str(c) + "-->" +str(x))
            x = x + 1
        else:
            if image_similarity_vectors_via_numpy(im, ex_im) > FAMILIAR_FRAME_PERCENTAGE:
                print("PASSED: " + str(c))
                os.remove(path + str(c) + '.jpg')
            else:
                ex_im = im
                im.save(path + str(x) + '.jpg')
                os.remove(path + str(c) + '.jpg')                
                print("RECORD: " + str(c) + "-->" +str(x))
                x = x + 1
    c = c + 1
vc.release()

