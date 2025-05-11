from ultralytics import YOLO
import cv2
import serial



arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)
model = YOLO('C:\MyModel\modelv4.pt')
cap = cv2.VideoCapture(1) # Open the camera, arg might change depending on the system.
lastcolor = 0


def transmitDetection(data):
  arduino.write(f'{data}\n'.encode())

def detectAndClassify():
  ret, frame = cap.read()
  if not ret:
    return "error"

  results = model(frame)
  detected_labels = []

  for box in results[0].boxes:
    cls_id = int(box.cls[0])
    label = model.names[cls_id]
    confidence = float(box.conf[0])
    xyxy = box.xyxy[0].cpu().numpy().astype(int)
    x1, y1, x2, y2 = xyxy
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    text = f"{label} ({confidence:.2f})"
    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    current = [label, confidence]
    detected_labels.append(current)
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      return "exit"
    for labels in detected_labels:
      if labels[1] > 0.80:
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
  print("output bin =" + str(output_bin))
  if(lastcolor != color): # this is to limit the amount of data sent to the arduino to avoid problems.
    transmitDetection(output_bin)
  lastcolor = color
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()