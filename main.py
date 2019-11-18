import cv2

initial_frame = None

video = cv2.VideoCapture(0)
while True:
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if initial_frame is None:
        initial_frame = gray
        continue

    delta_frame = cv2.absdiff(initial_frame, gray)

    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    cv2.imshow("Capturing", frame)
    cv2.imshow("Delta Image", delta_frame)
    key = cv2.waitKey(1)
    if key == ord('w'):
        break
video.release()
cv2.destroyAllWindows()