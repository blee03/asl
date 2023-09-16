import mediapipe as mp
import numpy as np
import cv2 as cv

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
  cam = cv.VideoCapture(0)
  if not cam.isOpened():
    print("error opening camera")
    exit()
  while True:
    # Capture frame-by-frame
    ret, frame = cam.read()
    # if frame is read correctly ret is True
    if not ret:
        print("error in retrieving frame")
        break
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    cv.imshow('frame', img)

    
    if cv.waitKey(1) == ord('q'):
        break

  cam.release()
  cv.destroyAllWindows()
  # Create a loop to read the latest frame from the camera using VideoCapture#read()

  # Convert the frame received from OpenCV to a MediaPipe’s Image object.

