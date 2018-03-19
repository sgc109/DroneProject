import cv2
import time
import requests
import json
import base64

size = 4
webcam = cv2.VideoCapture(0) #Use camera 0
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


timeGap =20 
cnt = 0


url = "http://localhost:10000/jsonrpc"
headers = {'content-type': 'application/json'}


while True:
    (rval, im) = webcam.read()
    im=cv2.flip(im,1,0) #Flip to act as a mirror

    # Resize the image to speed up detection
    mini = cv2.resize(im, (im.shape[1] / size, im.shape[0] / size))

    # detect MultiScale / faces 
    faces = classifier.detectMultiScale(mini)

    exist = None

    for f in faces:
        '''
        (x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
        cv2.rectangle(im, (x, y), (x + w, y + h),(0,255,0),thickness=4)
        '''
        exist = True

        
    if exist is not True:
        print('No faces!')

    else:
        cnt = (cnt + 1) % timeGap
        print('Face detected!')
        if cnt % timeGap is 0:
            path = 'clientPic/face'+str(time.time())+'.jpg' 
            cv2.imwrite(path, im)
            fp = open(path,'rb')
            print('Sending...')

            l = fp.read(2**20)
            payload = {
                "method": "isAlive",
                "params": [str(base64.b64encode(l))],
                "jsonrpc": "2.0",
                "id": 0,
            }
            
            response = requests.post(
                url, data=json.dumps(payload), headers=headers).json()

            fp.close()
            print("Done Sending")



    cv2.imshow('BCU Research by Waheed Rafiq (c)',   im)
    key = cv2.waitKey(10)
    # if Esc key is press then break out of the loop 
    if key == 27: #The Esc key
        break
