import mediapipe as mp
import numpy as np
import cv2 as cv

def cap1():
   import numpy as np
import cv2 as cv
cap = cv.VideoCapture(-1)
if not cap.isOpened():
 print("Cannot open camera")
 exit()
while True:
 # Capture frame-by-frame
 ret, frame = cap.read()
 # if frame is read correctly ret is True
 if not ret:
  print("Can't receive frame (stream end?). Exiting ...")
 break
 # Our operations on the frame come here
 gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
 # Display the resulting frame
 cv.imshow('frame', gray)
 if cv.waitKey(1) == ord('q'):
  break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('gesture recognition result: {}'.format(result))

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='./gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
with GestureRecognizer.create_from_options(options) as recognizer:
  # The detector is initialized. Use it here.
  # ...

  # Use OpenCV’s VideoCapture to start capturing from the webcam.
  cap1()
  # Create a loop to read the latest frame from the camera using VideoCapture#read()

  # Convert the frame received from OpenCV to a MediaPipe’s Image object.

