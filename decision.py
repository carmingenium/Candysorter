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
import time
import serial

# Connect to Arduino (adjust the port and baudrate to match your setup)
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
# set bin state to 0 (default bin)
inputstate = 0  # 0, 90, 180, 270 - should go between these values - should be tested to see which way it rotates
binstate = 0  # 0 = default bin, 1 = red, 2 = yellow, 3 = blue, 4 = green, 5 = brown, 6 = orange
# 0, 51.42, 102.84, 154.26, 205.68, 257.1, 308.52 - should go between these values - should be tested to see which way it rotates - 360/7 per unit - 51.42 degrees per bin
# load model

model = YOLO('model.pt')
cap = cv2.VideoCapture(0) # Open the camera (0 is default, should be tested and changed!)









# Rotation commands sent to Arduino
def rotate_90(): #deprecated
  global inputstate
  inputstate += 90
  if inputstate >= 360:
    inputstate = 0
  arduino.write(f'{inputstate}\n'.encode()) # NOT TESTED!
  # arduino.write(inputstate.encode())
  time.sleep(1)
  
def rotate_bin(bin_num): #deprecated
  global binstate
  binstate = float(bin_num * 51.42)
  arduino.write(f'{binstate}\n'.encode()) # NOT TESTED!
  # arduino.write(binstate.encode()) 
  time.sleep(1)
    
def get_color(): # NOT TESTED!
  ret, frame = cap.read()
  if not ret:
    return "error"
  results = model(frame)
  
  detected_labels = []
  for box in results[0].boxes:
    cls_id = int(box.cls[0])  # class index
    label = model.names[cls_id]
    detected_labels.append(label)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    return "error"
  return detected_labels[0] if detected_labels else "error" # burdaki logic değişecek, yanlış okumayla default çıkma olasılığı var o yüzden herhangi bir renk görünürse onu yollayacak şekilde düzeltilecek

def color_to_bin(color): 
  return { # should be ordered in the order of the bins to set rotation logic
    "red": 1,
    "yellow": 2,
    "blue": 3,
    "green": 4,
    "brown": 5,
    "orange": 6
  }.get(color, 0)
  
  # ^^^^^^^^^^^^^^^ yerleştirilmesi lazım
  # if(color==0)  // non m&m
  #   if(color==1)   // red
  #   if(color==2) // blue
  #   if(color==3) // orange
  #   if(color==4)   // yellow
  #   if(color==5)   // brown
  #   if(color==6)  // green


time.sleep(5)  # Wait for first input to be ready
rotate_90()  # Step 1: Input → Store
time.sleep(1)  # Simulate time taken to get new input
rotate_90()  # Step 2: Store → Camera
time.sleep(1)  # Simulate time taken to process input


# Main loop to simulate operation
while True:

  color = get_color()
  if color == "error":
    print("Error reading color")
    continue
  
  output_bin = color_to_bin(color) # 0,1,2,3,4,5,6 yollanıyor ama arduinoda açısıyla çarpılmış halde. modeldeki açıların verisi olmadığı için hatalı
  # led indication(color)  # Simulate LED indication (not implemented here)
  
  rotate_bin(output_bin)
  time.sleep(2) # Wait for bin rotation
  
  # Release time expectation
  time.sleep(1)
  
  # After release, go back to default bin.
  rotate_bin(0)
  time.sleep(2)  # Wait for bin rotation
  
  
  rotate_90() # Start next cycle
  
  # program stopping condition
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()