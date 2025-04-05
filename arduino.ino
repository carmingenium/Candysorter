Servo myservo;

void setup() {
  myservo.attach(9); // Attach the servo on pin 9 to the servo object
  Serial.begin(9600); // Start the serial communication at 9600 baud rate
  Serial.println("Ready");
  // to ensure right detection has been made
  pinMode(2, OUTPUT); // NONTARGET - DEFAULT
  pinMode(3, OUTPUT); // BLUE
  pinMode(4, OUTPUT); // YELLOW
  pinMode(5, OUTPUT); // GREEN
  pinMode(6, OUTPUT); // BROWN
  pinMode(7, OUTPUT); // RED
  pinMode(8, OUTPUT); // ORANGE
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read string until newline
    float rotation = input.toFloat();

    // to ensure right detection has been made 
    // # 0, 51.42, 102.84, 154.26, 205.68, 257.1, 308.52
    if (rotation == 0) {
      digitalWrite(2, HIGH); // NONTARGET - DEFAULT
      digitalWrite(3, LOW); // BLUE
      digitalWrite(4, LOW); // YELLOW
      digitalWrite(5, LOW); // GREEN
      digitalWrite(6, LOW); // BROWN
      digitalWrite(7, LOW); // RED
      digitalWrite(8, LOW); // ORANGE
    } else if (rotation == 51.42) {
      digitalWrite(2, LOW); // NONTARGET - DEFAULT
      digitalWrite(3, HIGH); // BLUE
      digitalWrite(4, LOW); // YELLOW
      digitalWrite(5, LOW); // GREEN
      digitalWrite(6, LOW); // BROWN
      digitalWrite(7, LOW); // RED
      digitalWrite(8, LOW); // ORANGE
    } else if (rotation == 102.84) {
      digitalWrite(2, LOW); // NONTARGET - DEFAULT
      digitalWrite(3, LOW); // BLUE
      digitalWrite(4, HIGH); // YELLOW
      digitalWrite(5, LOW); // GREEN
      digitalWrite(6, LOW); // BROWN
      digitalWrite(7, LOW); // RED
      digitalWrite(8, LOW); // ORANGE
    } else if (rotation == 154.26) {
      digitalWrite(2, LOW); // NONTARGET - DEFAULT
      digitalWrite(3, LOW); // BLUE
      digitalWrite(4, LOW); // YELLOW
      digitalWrite(5, HIGH); // GREEN
      digitalWrite(6, LOW); // BROWN
      digitalWrite(7, LOW); // RED
      digitalWrite(8, LOW); // ORANGE
    } else if (rotation == 205.68) {
      digitalWrite(2, LOW); // NONTARGET - DEFAULT
      digitalWrite(3, LOW); // BLUE
      digitalWrite(4, LOW); // YELLOW
      digitalWrite(5, LOW); // GREEN
      digitalWrite(6, HIGH); // BROWN
      digitalWrite(7, LOW); // RED
      digitalWrite(8, LOW); // ORANGE
    } else if (rotation == 257.1) {
      digitalWrite(2, LOW); // NONTARGET - DEFAULT
      digitalWrite(3, LOW); // BLUE
      digitalWrite(4, LOW); // YELLOW
      digitalWrite(5, LOW); // GREEN
      digitalWrite(6, LOW); // BROWN
      digitalWrite(7, HIGH); // RED
      digitalWrite(8, LOW); // ORANGE
    } else if (rotation == 308.52) {
      digitalWrite(2, LOW); // NONTARGET - DEFAULT
      digitalWrite(3, LOW); // BLUE
      digitalWrite(4, LOW); // YELLOW
      digitalWrite(5, LOW); // GREEN
      digitalWrite(6, LOW); // BROWN
      digitalWrite(7, LOW); // RED
      digitalWrite(8, HIGH); // ORANGE
    }



    if (rotation >= 0 && rotation <= 360) { // Ensure the value is within the servo range
      myservo.write(rotation);
      Serial.print("Servo rotated to: ");
      Serial.println(rotation);
    } else {
      Serial.println("Invalid angle.");
    }
  }
}