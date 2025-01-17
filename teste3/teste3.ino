#include <Servo.h>

Servo serX;
Servo serY;

void setup() {
  serX.attach(10);
  serY.attach(11);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String serialData = Serial.readStringUntil('\n'); // Lê até a nova linha, melhora a leitura
    moveServos(serialData);
  }
}

void moveServos(String data) {
  int xIndex = data.indexOf('X');
  int yIndex = data.indexOf('Y');

  if (xIndex != -1 && yIndex != -1) {
    int xValue = data.substring(xIndex + 1, yIndex).toInt();
    int yValue = data.substring(yIndex + 1).toInt();

    xValue = constrain(xValue, 0, 180);
    yValue = constrain(yValue, 0, 180);

    serX.write(xValue);
    serY.write(yValue);
  }
}
