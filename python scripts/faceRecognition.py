import os
import cv2
import numpy as np
from PIL import Image
import random
import threading
import time

class faceRecognition:

    def __init__(self):

        self.cam = cv2.VideoCapture(0)
        self.detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.recognizer = cv2.createLBPHFaceRecognizer()
        self.path = "dataSet"

    def setTextColor(self):
        self.font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
        return self.font


    def TrainModel(self):

        Id = random.randint(1,101)

        sampleNum=0

        while(True):

            ret, img = self.cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, 1.3, 5)
            name = raw_input("Enter your name on the Keyboard : ")
            os.makedirs("/home/pi/Raspberry Project/dataSet/"+name,0777)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                
                #incrementing sample number 
                sampleNum = sampleNum + 1

                #saving the captured face in the dataset folder
                os.makedirs(name)
                cv2.imwrite("dataSet/"+name+"User."+ str(Id) +'.'+ str(sampleNum) + ".jpg", gray[y:y+h+10,x:x+w+10])

                cv2.imshow('frame',img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 20
            elif sampleNum > 11:
                break
        self.cam.release()
        cv2.destroyAllWindows()

    def createImageIds(self):

        imagePaths = [os.path.join(self.path,f) for f in os.listdir(self.path)]
        faces = []
        ids = []

        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert("L")
            faceNp = np.array(faceImg, 'uint8')
            id = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            ids.append(id)
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)

        return ids, faces

    def Detector(self):

        while True:

            ret , im = self.cam.read()

            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

            faces = self.detector.detectMultiScale(gray, 1.2,5)

            for(x,y,w,h) in faces:
                
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)

                Id, conf = self.recognizer.predict(gray[y:y+h,x:x+w])

                if(conf<50):
                    if(Id==16):
                        Id="Mxolisi"
                    elif(Id==52):
                        Id="Sibusiso"
                else:
                    Id="Unknown"
            cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),self.font, 255)
            cv2.imshow('im',im) 
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    def main():
        pass
    
    if __name__ == '__main__':
        main()

Ids , faces = createImageIds(self.path)
recognizer.train(faces, np.array(Ids))
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
