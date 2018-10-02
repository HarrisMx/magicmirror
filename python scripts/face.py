import cv2
import time
import numpy as np
from threading import Thread
 
 

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath)

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX


class CameraInst():
        # Constructor...
        def __init__(self):
                fps        = 25.0               # Frames per second...
                resolution = (640, 480)         # Frame size/resolution...
                w = 640
                h = 480
 
                self.cap = cv2.VideoCapture(0)  # Capture Video...
                print("Camera warming up ...")
                time.sleep(1)
 
                # Define the codec and create VideoWriter object
                #fourcc = cv2.VideoWriter_fourcc(*"H264")
                fourcc = cv2.cv.CV_FOURCC(*"H264")
                # You also can use (*'XVID')
                self.out = cv2.VideoWriter('output.avi',fourcc, fps, (w, h))
 
        def captureVideo(self):
                # Capture
                self.ret, self.frame = self.cap.read()
                # Image manipulations come here...
                self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                 
                faces = faceCascade.detectMultiScale(self.gray, scaleFactor = 1.5, minNeighbors = 5)

                for (x , y , w , h) in faces:
                    print(x , y , w , h)
                    roi_gray = self.gray[ y : y + h + 15, x : x + w + 15]
                    roi_color = self.frame[ y : y + h , x : x + w ]
                    cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    cv2.imwrite("image.png", roi_gray)
                    

                cv2.imshow('Face Recognition',self.gray) 

        def drawShape(self):
                pass

        def saveVideo(self):
                # Write the frame
                self.out.write(self.frame)
 
        def __del__(self):
                self.cap.release()
                cv2.destroyAllWindows()
                print("Camera disabled and all output windows closed...")
 
def main():
        cam1 = CameraInst()
        
        while(True):   

                # Display the resulting frames...
                cam1.captureVideo() # Live stream of video on screen...
                #cam1.saveVideo() # Save video to file 'output.avi'...
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
 
if __name__=='__main__':
        main()