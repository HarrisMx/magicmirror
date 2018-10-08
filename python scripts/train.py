import cv2
import os
import random

cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

Id = random.randint(1,101)

images = []

sampleNum=0

name = raw_input("Enter your name on the Keyboard : ")

os.makedirs("/home/pi/Raspberry Project/dataSet/"+name,0777)


while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        #incrementing sample number 
        sampleNum = sampleNum + 1
        #saving the captured face in the dataset folder
        image = "dataSet/"+name+"/"+"User."+ str(Id) +'.'+ str(sampleNum) + ".jpg"
        images.append(image)
        cv2.imshow('frame',img)
    #wait for 15 miliseconds
    if cv2.waitKey(15) & 0xFF == ord('q'):
        for image in images:
            cv2.imwrite(image, gray[y:y+h+10,x:x+w+10])
            print(image)
        break
        
    # break if the sample number is morethan 20
    elif sampleNum > 11:
        for image in images:
            cv2.imwrite(image, gray[y:y+h+10,x:x+w+10])
        break
    
cam.release()
cv2.destroyAllWindows()