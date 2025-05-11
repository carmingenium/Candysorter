from ultralytics import YOLO
import cv2
import serial


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
# load model and camera
model = YOLO('model.pt')
cap = cv2.VideoCapture(1) # Open the camera, arg might change depending on the system.

def transmitDetection(data):
  arduino.write(f'{data}\n'.encode()) # Send data to Arduino

def detectAndClassify():
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
    return "exit"
  # all detected objects are on the list.
  for labels in detected_labels:
    if labels[1] > 0.80:   # if there is any with confidence over 80%, return it.
      return labels[0]
  return "default"

def color_to_bin(color): # There is no need to add another bin for default, as any input outside the list will default to 0 bin.
  return {
    "red": 1,
    "blue": 2,
    "orange": 3,
    "yellow": 4,
    "brown": 5,
    "green": 6
  }.get(color, 0)

while True:

  color = detectAndClassify()
  if color == "error":
    print("Error reading color")
    continue
  output_bin = color_to_bin(color)
  transmitDetection(output_bin)  # LCD is handled from this data in Arduino also.
  # program stopping condition
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()