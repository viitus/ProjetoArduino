import pygame
import serial

# Configurações da comunicação serial
arduino_port = 'COM3'  # Substitua pela porta correta do seu Arduino
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# Inicializando o Pygame
pygame.init()

# Configurações da janela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Controle dos Servos com Mouse')

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Captura a posição do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Converte a posição do mouse para os valores esperados pelo Arduino (0 a 180)
    servo_x = int((mouse_x / screen_width) * 180)
    servo_y = int((mouse_y / screen_height) * 180)

    # Envia os valores para o Arduino no formato "X{valor}Y{valor}\n"
    command = f"X{servo_x}Y{servo_y}\n"
    arduino.write(command.encode('utf-8'))

    # Atualiza a tela (pode ser usada para adicionar gráficos futuramente)
    screen.fill((30, 30, 30))
    pygame.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), 10)
    pygame.display.flip()

# Encerra a comunicação e o Pygame
arduino.close()
pygame.quit()
