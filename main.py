import cv2, pandas
from datetime import datetime

initial_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=['Start', 'End'])

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if initial_frame is None:
        initial_frame = gray
        continue

    delta_frame = cv2.absdiff(initial_frame, gray)
    threshold_frame = cv2.threshold(delta_frame, 80, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations= 2)
    
    (cnts,_) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    status_list.append(status)
    
    status_list = status_list[-2:]
    
    
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
    
    cv2.imshow("Capturing", frame)
    cv2.imshow("Gray Blurred", gray)
    cv2.imshow("Delta Image", delta_frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    
    
    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({'Start' : times[i], 'End' : times[i + 1]}, ignore_index = True)

df.to_csv("times.csv")

video.release()
cv2.destroyAllWindows()