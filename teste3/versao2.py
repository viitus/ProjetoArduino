import pygame
import serial
import pyautogui
import time

# Configuração da porta serial
arduino_port = 'COM3'
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# Inicializa o Pygame
pygame.init()

# Obtém as dimensões da tela
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Cria uma janela de jogo em tela cheia
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption('Controle dos Servos com Mouse')

# Centraliza o mouse na tela ao iniciar
screen_x, screen_y = 0, 0
pyautogui.moveTo(screen_x + screen_width // 2, screen_y + screen_height // 2)

# Variáveis para rastrear o estado do laser e do mouse
laser_on = False
last_mouse_x, last_mouse_y = pygame.mouse.get_pos()
last_sent_time = time.time()

# Loop principal do programa
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Detecta clique do mouse
            laser_on = not laser_on  # Alterna o estado do laser
            laser_state = "1" if laser_on else "0"
            command = f"L{laser_state}\n"  # Envia comando para ligar/desligar o laser
            arduino.write(command.encode('utf-8'))
            arduino.flush()

    # Captura a posição atual do mouse
    current_mouse_x, current_mouse_y = pygame.mouse.get_pos()

    # Verifica se o mouse foi movido desde a última leitura
    if current_mouse_x != last_mouse_x or current_mouse_y != last_mouse_y:
        current_time = time.time()

        # Envia comandos a cada 30ms para evitar sobrecarga da comunicação
        if current_time - last_sent_time > 0.03:
            servo_x = int(180 - (current_mouse_x / screen_width) * 180)  # Inverte o eixo X
            servo_y = int((current_mouse_y / screen_height) * 180)

            command = f"X{servo_x}Y{servo_y}\n"
            arduino.write(command.encode('utf-8'))
            arduino.flush()

            last_sent_time = current_time
            last_mouse_x, last_mouse_y = current_mouse_x, current_mouse_y

    # Reposiciona o mouse no centro da tela
    pyautogui.moveTo(screen_x + screen_width // 2, screen_y + screen_height // 2)

    # Atualiza a janela do Pygame
    screen.fill((30, 30, 30))  # Preenche a tela com uma cor cinza escuro
    pygame.draw.circle(screen, (255, 0, 0), (current_mouse_x, current_mouse_y), 10)  # Indicador de posição
    pygame.display.flip()

# Fecha a comunicação e encerra o Pygame
arduino.close()
pygame.quit()
