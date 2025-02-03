#include <Servo.h>

// Definindo os pinos
const int servoXPin = 11; // Pino do servo no eixo X
const int servoYPin = 10; // Pino do servo no eixo Y
const int laserPin = 12;  // Pino do laser

// Criando objetos para os servos
Servo servoX;
Servo servoY;

void setup() {
  // Inicializa os servos
  servoX.attach(servoXPin);
  servoY.attach(servoYPin);

  // Configura o pino do laser como saída
  pinMode(laserPin, OUTPUT);

  // Desliga o laser inicialmente
  digitalWrite(laserPin, LOW);

  // Inicializa a comunicação serial
  Serial.begin(9600);
  Serial.println("Sistema inicializado. Aguardando comandos...");
}

void loop() {
  // Verifica se há dados disponíveis na porta serial
  if (Serial.available() > 0) {
    // Lê a string até o caractere de nova linha ('\n')
    String data = Serial.readStringUntil('\n');
    data.trim(); // Remove espaços em branco extras

    // Variáveis para armazenar os valores recebidos
    int x = 90; // Valor padrão para o eixo X
    int y = 90; // Valor padrão para o eixo Y
    int laser = 0; // Valor padrão para o laser (desligado)

    // Encontra as posições das vírgulas
    int firstComma = data.indexOf(',');
    int secondComma = data.indexOf(',', firstComma + 1);

    // Verifica se o formato dos dados está correto
    if (firstComma != -1 && secondComma != -1) {
      // Extrai os valores de X, Y e Laser da string
      x = data.substring(0, firstComma).toInt();
      y = data.substring(firstComma + 1, secondComma).toInt();
      laser = data.substring(secondComma + 1).toInt();

      // Limita os valores de X e Y aos intervalos permitidos
      x = constrain(x, -180, 180); 
      y = constrain(y, -180, 180);  

      // Move os servos para as posições especificadas
      servoX.write(x);
      servoY.write(y);

      // Controla o laser (1 = ligado, 0 = desligado)
      digitalWrite(laserPin, laser == 1 ? HIGH : LOW);

      // Exibe os valores recebidos no monitor serial para depuração
      Serial.print("X: "); Serial.print(x);
      Serial.print(" | Y: "); Serial.print(y);
      Serial.print(" | Laser: "); Serial.println(laser);
    } else {
      // Se o formato dos dados estiver incorreto, exibe uma mensagem de erro
      Serial.println("Erro: Formato de dados inválido!");
    }
  }
}