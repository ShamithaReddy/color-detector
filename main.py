import pandas as pd
import cv2
import sys
import math

img_path='colorpic.jpg'
csv_path='colors.csv'

df=pd.read_csv(csv_path)

index=['color','color_name','hex','R','G','B']
df=pd.read_csv(csv_path,names=index)


# Create window with freedom of dimensions
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
#image is read as a array of numbers
img=cv2.imread(img_path)
img=cv2.resize(img,(800,600))



clicked=False
r=g=b=xpos=ypos=0

#finding the minimum distance b/w the rgb value from image and the colour names we have
def get_color_name(R,G,B):
    minimum=10000
    for i in range(len(df)):
        d=math.sqrt((R-int(df.loc[i,'R']))*(R-int(df.loc[i,'R']))+(G-int(df.loc[i,'G']))*(G-int(df.loc[i,'G']))+(B-int(df.loc[i,'B']))*(B-int(df.loc[i,'B'])))
        if d<minimum:
            minimum=d
            colorname=df.loc[i,'color_name']
    return(colorname)
   

def draw_function(event,x,y,flags,parameters):
    if event==cv2.EVENT_LBUTTONDBLCLK:
        global clicked,r,g,b,xpos,ypos
        clicked=True
        xpos=x
        ypos=y
        b,g,r=img[y,x]
        #b is a numpy value, as the image stores the pixels in a numpy array
        b=int(b)
        g=int(g)
        r=int(r)
        


#creating a window
#cv2.namedWindow('image')

cv2.setMouseCallback('image',draw_function)



#cv2.getWindowProperty() returns -1 as soon as the window is closed.
#0 is the flag with Full screen property, it becomes -1 when the window is closed 
while cv2.getWindowProperty('image', 0) >= 0:
    keyCode = cv2.waitKey(30)
    cv2.imshow('image',img)
    if clicked:
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) 
        #Thickness of -1 px will fill the rectangle shape by the specified color.
        cv2.rectangle(img,(20,20),(750,60),(b,g,r),-1)
        text=get_color_name(r,g,b)+' R='+str(r)+' G='+str(g)+' B='+str(b)
        #cv2.putText(image, text, org, font_Type, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        #org is the coordinates of the bottom-left corner of the text string in the image.
        cv2.putText(img,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2,cv2.LINE_AA)
        if r+g+b>=600:
            #if the color is too light then we write the text in black
            cv2.putText(img,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),2,cv2.LINE_AA)
    #this waitkey tells the window to close when clicked esc button
    if cv2.waitKey(30) and 0xFF==27:
        break


cv2.destroyAllWindows()







