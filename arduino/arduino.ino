// LCD SETUP
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
String colorName = "";
// LCD SETUP END

#include <Stepper.h>
int state=0;
int color=0;
int sayac=0 ;
const int stepsPerRevolution = 2048; // 28BYJ-48 için tam tur adım sayısı
Stepper myStepper1(stepsPerRevolution, 8, 10, 9, 11); // Bağlantı pinleri
Stepper myStepper2(stepsPerRevolution, 4, 6, 5, 7);


void setup() {
  myStepper1.setSpeed(5); // Motor hızını 10 RPM olarak ayarla
  myStepper2.setSpeed(5); // Motor hızını 10 RPM olarak ayarla
  Serial.begin(9600); // Serial iletişim başlat, 9600 baud
  lcd.init();
  lcd.backlight();
}

void loop() {
  if(state==0){
  myStepper1.step(-512);
  delay(100);
  state++;
  }

  if(state==1){
    if (Serial.available() > 0) {
      color = Serial.parseInt(); // Girilen sayıyı oku
      // LCD COLOR PRINT BEFORE STEPPER
      if (color >= 0 && color <= 6) {
        colorName = codeToColor(color);
        lcd.setCursor(0, 0);    
        lcd.print("Color:         "); 
        lcd.setCursor(0, 0);
        lcd.print("Color: " + colorName);
      // LCD COLOR PRINT BEFORE STEPPER END
      }
      while (Serial.available() > 0 && Serial.peek() != '\n' && Serial.peek() != '\r') {
        Serial.read(); // Sayıdan sonraki sayısal olmayan karakterleri oku ve at
      }
      if (Serial.available() > 0) {
        Serial.read(); // Satır sonu karakterini oku ve at
      }
    }
  if(color==0) { myStepper2.step((color-sayac)*293); sayac = 0; }  // non m&m
  if(color==1)  {myStepper2.step((color-sayac)*293); sayac = 1;}  // red
  if(color==2) { myStepper2.step((color-sayac)*293); sayac = 2;}  // blue
  if(color==3){myStepper2.step((color-sayac)*293); sayac = 3;}  // orange
  if(color==4) { myStepper2.step((color-sayac)*293); sayac = 4;}  // yellow
  if(color==5) { myStepper2.step((color-sayac)*293); sayac = 5;}  // brown
  if(color==6)  {myStepper2.step((color-sayac)*293); sayac = 6;}  // green
  state=0;
  }
}
// LCD FUNCTION
String codeToColor(int code) {
  switch (code) {
    case 1: return "red";
    case 2: return "blue";
    case 3: return "orange";
    case 4: return "yellow";
    case 5: return "brown";
    case 6: return "green";
    default: return "Default";  // 0 or invalid cases
  }
}
// LCD FUNCTION END