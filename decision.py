# 4 holes: input, store, camera, output
# from input we get objects in queue, continiously.
# we rotate the machine 90 degrees so object in the input hole goes to store hole. we get another input at that moment.
# from store rotate another 90 degrees so the stored object goes to camera hole, input goes to store, from queue we get another input.
# at this point, camera detects the object in camera hole and selects the right output hole
# we rotate the machine 90 degrees so the object in camera hole goes to output hole and all the other objects take another step.

# counter clockwise 90 degrees.
# after every decision we go to default hole for the output hole.

from ultralytics import YOLO
import cv2
import time # can be used later for timing the rotation of the machine
import serial

# Connect to Arduino (adjust the port and baudrate to match your setup)
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

# load model and camera
model = YOLO('model.pt')
cap = cv2.VideoCapture(0) # Open the camera (0 is default, should be tested and changed!)

def send_data(data):
  arduino.write(f'{data}\n'.encode()) # Send data to Arduino
  
def get_color(): # NOT TESTED!
  ret, frame = cap.read()
  if not ret:
    return "error" # goes to default if loop continues
  results = model(frame)
  
  detected_labels = []
  for box in results[0].boxes:
    cls_id = int(box.cls[0])  # class index
    label = model.names[cls_id]
    confidence = float(box.conf[0])  # confidence score
    detected_labels.append(label,confidence)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    return "exit" # goes to default if loop continues
  
  # all detected objects are on the list.
  for labels in detected_labels:
    if labels[1] > 0.80:   # if there is any with confidence over 80%, return it.
      return labels[0]
  return "default"  # else return default
 
def color_to_bin(color): 
  return {
    "red": 1,
    "blue": 2,
    "orange": 3,
    "yellow": 4,
    "brown": 5,
    "green": 6
  }.get(color, 0)
  
# Main loop to simulate operation
# need to define a way to run color detection on the right time. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# maybe we can use a timer a bit shorter than the waiting time of the motors at every slot to make sure it will send data once, but excess data may become a problem. 
while True:

  color = get_color()
  if color == "error":
    print("Error reading color")
    continue
  
  output_bin = color_to_bin(color)
  # lcd indication(color)  # Simulate LCD indication (not implemented here)
  send_data(output_bin)  # Send the color to Arduino
  
  # program stopping condition
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()