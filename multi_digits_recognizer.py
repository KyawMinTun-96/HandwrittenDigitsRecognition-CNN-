#import required library
from keras.models  import load_model
import numpy as np
import cv2


#load your model here MNIST-CNN.model
model = load_model("model/mnistCNN.h5")


cap = cv2.VideoCapture(0)
if(cap.isOpened()):
    while(True):

        #read frame frame from video
        ret, image = cap.read()
        img2 = image.copy()

        #perform basic operation to smooth image
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 0)

        #find threshold
        ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        #find contours and draw contours
        _, ctrs, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        #cv2.drawContours(source image, contour,contour index means:To draw all contours for add -1, color, thickness)
        cv2.drawContours(image, ctrs, -1,(255, 255, 0), 2)
        rects = [cv2.boundingRect(ctr) for ctr in ctrs]


        for rect in rects:
            x,y,w,h = rect
            if  h > 50 and h < 300  or w > 10 :

                #draw rectangel on image
                cv2.rectangle(img2, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (36, 255, 12), 1)
                leng = int(rect[3] * 1.6)
                pt1 = abs(int(rect[1] + rect[3] // 2 - leng // 2))
                pt2 = abs(int(rect[0] + rect[2] // 2 - leng // 2))
                roi = img[pt1:pt1+leng, pt2:pt2+leng]

                #resize image
                roi = cv2.resize(roi,(28, 28), interpolation=cv2.INTER_AREA)
                #cv2.imshow('invert image',roi)#new line
                roi = roi.reshape(-1,28, 28, 1)
                roi = np.array(roi, dtype='float32')
                roi /= 255



                pred_array = model.predict(roi)[0]
                final_array = np.argmax(pred_array)
                result = str(final_array) +' ' +str(int(max(pred_array) * 100))+'%'               
                cv2.putText(img2, result, (rect[0], rect[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 25), 2)
                
        #show frame
        cv2.imshow("Result",img2)
        cv2.imshow("Thresh",img)

        key = cv2.waitKey(1)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('c'):
            cv2.imwrite('result_image/capture.jpg',img2)
            break
cap.release()
cv2.destroyAllWindows()