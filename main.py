from flask import Flask, render_template
import cv2
from datetime import datetime
import winsound

app = Flask(__name__,template_folder = "templates")

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/start-recording')
def start_recording():
  record()
  return Flask.redirect('/')
# http://100.75.232.158:8080/video

def record():
    # Create a VideoCapture object and open the webcam.
  cap = cv2.VideoCapture('http://192.168.16.215:8080/video')

# Create a VideoWriter object and open a new video file for writing.
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  out = cv2.VideoWriter('recordings/' + datetime.now().strftime("%H-%M-%S") + '.avi', fourcc,20.0,(640,480))

# Enter an infinite loop.
  while True:

    # Read the next frame from the webcam.
    _, frame = cap.read()

    # Write the frame to the video file.
    out.write(frame)

    # Display the frame in a window.
    cv2.imshow("esc. to stop", frame)

    # Check if the user has pressed the `Esc` key.
    if cv2.waitKey(1) == 27:

        # Break out of the loop.
        break

# Release the webcam.
  cap.release()

# Close all open windows.
cv2.destroyAllWindows()

  
@app.route('/monitor')
def monitor():
  monitor()
  return Flask.redirect('/')

def monitor():
   # Create a VideoCapture object and open the webcam.
  # Create a VideoCapture object and open the webcam.
  cam = cv2.VideoCapture('http://192.168.16.215:8080/video')

  while cam.isOpened():

    # Capture two frames from the webcam.
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()

    # Calculate the difference between the two frames.
    diff = cv2.absdiff(frame1, frame2)

    # Convert the difference image to grayscale.
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    # Blur the grayscale image.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the blurred image to create a binary image.
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate the binary image to fill in any small gaps.
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find the contours in the dilated image.
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original frame.
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    # Iterate through the contours and find any large objects.
    for c in contours:

        # Check if the contour is large enough.
        if cv2.contourArea(c) < 5000:
            continue

        # Get the bounding rectangle of the contour.
        x, y, w, h = cv2.boundingRect(c)

        # Draw a rectangle around the object in the original frame.
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Play an alert sound.
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

    # Display the original frame.
    cv2.imshow('Granny Cam', frame1)

    # Check if the user has pressed the `q` key.
    if cv2.waitKey(10) == ord('q'):
        break

# Release the webcam.
  cam.release()

# Close all open windows.
cv2.destroyAllWindows()



if __name__ == '__main__':
  app.run(debug=True)
