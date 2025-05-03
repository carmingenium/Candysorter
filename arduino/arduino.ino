#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // 0x3F olabilir

String inputColor = "red";

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  
  displayColor(inputColor);
}

void loop() {

}

void displayColor(int color) {
  String colorOutput = colorToBin(color);

  lcd.setCursor(0, 0);
  lcd.print("Color: " + colorOutput);

  lcd.setCursor(0, 1);
  lcd.print("Code: " + String(color));
}

int colorToBin(String color) {
  if (color == 1) return "red";
  if (color == 2) return "blue";
  if (color == 3) return "orange";
  if (color == 4) return "yellow";
  if (color == 5) return "brown";
  if (color == 6) return "green";
  return "default";
}