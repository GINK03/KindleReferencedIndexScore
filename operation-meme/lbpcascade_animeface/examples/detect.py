import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import os.path
# for mac

def detect(filename, cascade_file = "../lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (24, 24))
    import random
    import time
    for (x, y, w, h) in faces:
        #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        image = image[y:y+h, x:x+w]
        try:
          image = cv2.resize(image, (96, 96) )
          #cv2.imshow("AnimeFaceDetect", image)
          #cv2.waitKey(0)
          cv2.imwrite("out" + str(time.time()) + ".png", image)
        except:
          pass

    
#detect(sys.argv[1])
import subprocess
res = subprocess.check_output(["find", "./comics"])
jpgs = filter(lambda x:'jpg' in x, [x for x in res.split('\n')] )
for jpg in jpgs:
  detect(jpg)
