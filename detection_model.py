import numpy as np 
import cv2
import dlib
from imutils import face_utils
from pygame import mixer
import pywhatkit as pwk
from twilio.rest import Client

cap=cv2.VideoCapture(0) # to capture live video through webcam
detector=dlib.get_frontal_face_detector() # to detect the face in frame

# here we are using a pre trained model to detect landmarks
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# variables used in our code
number=0
sleep_counter=0
drowsy_counter=0
active_counter=0
status_message=""
color1=(0,0,0)
color2=(0,0,0)
color3=(0,0,0)
textmessage="This is to bring to your notice that Driver in XXXXX vehicle is falling asleep"

# A function to calculate the euclidean distance between the coordinates of the landmarks
def euclidean_distance(ptA,ptB):
    dist=np.linalg.norm(ptA - ptB);
    return dist

# A function to calculate the EAR (Eye Aspect Ratio) and return the respective values
def eyes(a,b,c,d,e,f):
    up=euclidean_distance(b,d)+euclidean_distance(c,e)
    down=euclidean_distance(a,f)
    ratio1=up/(2.0*down)
    if(ratio1>0.28):
        return 2,ratio1
    elif(ratio1>0.24 and ratio1<=0.28):
        return 1,ratio1
    else:
        return 0,ratio1

# A function to calculate the MAR (Mouth Aspect Ratio) and return the respective values
def yawn(a,b,c,d,e,f,g,h):
    up=euclidean_distance(b,d)+euclidean_distance(c,e)+euclidean_distance(d,g)
    down=euclidean_distance(a,h)
    ratio2=up/(3.0*down)
    if(ratio2>0.33):
        return 1,ratio2
    else:
        return 0,ratio2


# The main code starts here where we find a face in the screen and process the frame
while True:
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  # convert to grayscale image
    faces=detector(gray)
    for face in faces:  # to recognise a face in a frame
        x1=face.left()
        y1=face.top()
        x2=face.right()
        y2=face.bottom()
        face_frame=frame.copy()
        cv2.rectangle(face_frame,(x1,y1),(x2,y2),(0,255,0),2)
        landmarks=predictor(gray,face)

        # A numpy function to convert landmarks into an array 
        landmarks=face_utils.shape_to_np(landmarks) 
        left_eye,ear_ratio=eyes(landmarks[36],landmarks[37],landmarks[38],landmarks[41],landmarks[40],landmarks[39])
        right_eye,ear_ratio=eyes(landmarks[42],landmarks[43],landmarks[44],landmarks[47],landmarks[46],landmarks[45])        
        mouth_mar,mar_ratio1=yawn(landmarks[60],landmarks[61],landmarks[62],landmarks[63],landmarks[67],landmarks[66],landmarks[65],landmarks[64])
        
        # Different cases to find whwether a person is drowsy, sleeping or acitve
        if(left_eye==0 or right_eye==0):
            sleep_counter+=1
            drowsy_counter=0
            active_counter=0

            # Checking for Sleepiness
            if(sleep_counter>40):
                status_message="Sleeping !!"
                number=number+1
                
               # To play the Buzzer
                mixer.init()
                sound=mixer.Sound("buzzer.mp3")
                sound.play()

                # To send a SMS to a phone number (use Twilio)
                account_sid="********************"
                auth_token="*********************"
                client=Client(account_sid,auth_token)
                message=client.messages.create(
                body="This is to bring to your notice that Driver in XXXXX vehicle is falling asleep",
                from_="********(phone number)",
                to="**********")
                print(message.sid)
               
                color1=(0,0,255)
                color2=(0,255,0)
                color3=(0,0,255)

        # Checking for Drowsiness
        elif((left_eye==1 or right_eye==1) or mouth_mar==1):
            sleep_counter=0
            active_counter=0
            drowsy_counter+=1
            if(left_eye==1 or right_eye==1):
                color1=(255,0,0)
                color2=(0,255,0)
            else:
                color2=(255,0,0)
                color1=(0,255,0)
            if(drowsy_counter>6):
                status_message="Drowsy"
                color3=(255,0,0)

        # Checking for activeness
        else:
            drowsy_counter=0
            sleep_counter=0
            active_counter+=1
            if(active_counter>6):
                status_message="Active"
                color1=(0,225,0)
                color2=(0,255,0)
                color3=(0,255,0)

        # To write on the output frames
        cv2.putText(frame,status_message,(20,150),cv2.FONT_HERSHEY_SIMPLEX,1.2,color3,3)
        cv2.putText(frame,"EAR : "+str(round(ear_ratio,3)),(20,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,color1,2)
        cv2.putText(frame,"MAR : "+str(round(mar_ratio1,3)),(20,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,color2,2)

        # To plot the landmarks customly
        for n in range(0,68):
            (x,y)=landmarks[n]
            cv2.circle(face_frame,(x,y),1,(255,0,0),-1)

        # To display the ouptuts on screen
        cv2.imshow("frame",frame)
        cv2.imshow("Output",face_frame)

    # To wait for the Program to end 
    key=cv2.waitKey(1)
    if key==27:
        break

# To release the capturing video and clear the displayed window
cap.release()
cv2.destroyAllWindows()



