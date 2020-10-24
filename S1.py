import cv2,pandas,datetime

frame1=None

aList= [None,None]

move = []
data = pandas.DataFrame(columns=["Started","Stopped"])
video = cv2.VideoCapture(0)
while True:
    see, frame = video.read()
    a=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if frame1 is None:
        frame1=gray
        continue
# calculate the diffrance between firstFrame and the currentFrame
    frame2=cv2.absdiff(frame1,gray)
    thresh=cv2.threshold(frame2, 30, 255, cv2.THRESH_BINARY)[1]
    thresh=cv2.dilate(thresh, None, iterations=3)

    (cs,_) =cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for count in cs:
        if cv2.contourArea(count) < 9000:
            continue
        a=1
        (x, y, w, h)=cv2.boundingRect(count)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
    aList.append(a)
    if aList[-1] ==1 and aList[-2]==0:
        move.append(datetime.datetime.now())
    if aList[-1] ==0 and aList[-2]==1:
        move.append(datetime.datetime.now())

    # cv2.imshow("gray", gray)
    # cv2.imshow("transparent",frame2)
    # cv2.imshow("Thresh",thresh)
    cv2.imshow("Color frame",frame)

    key=cv2.waitKey(1)
    if key==ord('q'):
        if a==1:
            move.append(datetime.datetime.now())
        break
for i in range(0,len(move),2):
    data=data.append({"Started":move[i],"Stopped":move[i+1]},ignore_index=True)

data.to_csv("./data.csv")

video.release()
cv2.destroyAllWindows