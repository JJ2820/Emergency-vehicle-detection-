import cv2
import datetime
import RPi.GPIO as GPIO
import time

# Set up GPIO pins for LED signals
green_led = 18
yellow_led = 24
red_led = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(yellow_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)

# Set up camera
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # Set width of video frame
camera.set(4, 480)  # Set height of video frame

# Function to detect traffic density based on license plates in the video frame
def get_traffic_density():
    num_plates = 0
    while num_plates < 3:  # Wait for at least 3 license plates to be detected
        # Read a frame from the camera
        _, frame = camera.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect license plates in the frame
        plates_cascade = cv2.CascadeClassifier('haarcascade_license_plate.xml')
        plates = plates_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw bounding boxes around the detected license plates
        for (x, y, w, h) in plates:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            num_plates += 1

            # Crop license plate region from the frame
            plate_img = frame[y:y+h, x:x+w]

            # Save license plate image to file with current date and time
            now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = 'plates/plate_{}.jpg'.format(now)
            cv2.imwrite(filename, plate_img)

        # Display the frame with license plate detections
        cv2.imshow("License Plate Detection", frame)
        cv2.waitKey(1)

    # Calculate traffic density based on the number of license plates detected
    if num_plates < 10:
        return "light"
    elif num_plates < 20:
        return "medium"
    else:
        return "heavy"

# Main traffic system loop
while True:
    # Set the traffic light to green
    GPIO.output(green_led, GPIO.HIGH)
    GPIO.output(yellow_led, GPIO.LOW)
    GPIO.output(red_led, GPIO.LOW)

    # Wait for traffic to clear the intersection
    time.sleep(5)

    # Get the traffic density
    traffic_density = get_traffic_density()

    # Set the traffic light based on traffic density
    if traffic_density == "light":
        # Set the traffic light to green
        GPIO.output(green_led, GPIO.HIGH)
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.output(red_led, GPIO.LOW)
        # Wait for some time before switching to yellow
        time.sleep(5)
        # Set the traffic light to yellow
        GPIO.output(green_led, GPIO.LOW)
        GPIO.output(yellow_led, GPIO.HIGH)
        GPIO.output(red_led, GPIO.LOW)
        # Wait for some time before switching to red
        time.sleep(2)
        # Set the traffic light to red
        GPIO.output(green_led, GPIO.LOW)
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.output(red_led, GPIO.HIGH)
    elif traffic_density == "medium
        # Wait for some time before switching to yellow
        time.sleep(5)
        # Set the traffic light to yellow
        GPIO.output(green_led, GPIO.LOW)
        GPIO.output(yellow_led, GPIO.HIGH)
        GPIO.output(red_led, GPIO.LOW)
        # Wait for some time before switching to red
        time.sleep(3)
        # Set the traffic light to red
        GPIO.output(green_led, GPIO.LOW)
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.output(red_led, GPIO.HIGH)
    else:
        # Set the traffic light to red
        GPIO.output(green_led, GPIO.LOW)
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.output(red_led, GPIO.HIGH)
        # Wait for some time before checking traffic density again
        time.sleep(10)
