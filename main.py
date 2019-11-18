import cv2

initial_frame = None

video = cv2.VideoCapture(0)
while True:
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if initial_frame is None:
        initial_frame = gray
        continue

    cv2.imshow("Capturing", frame)
    key = cv2.waitKey(1)
    if key == ord('w'):
        break
video.release()
cv2.destroyAllWindows()