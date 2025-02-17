import pygame
import serial
import pyautogui
import time
import cv2
import numpy as np

# Configuração da conexão com o Arduino
arduino_port = 'COM4'
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# Inicialização do Pygame
pygame.init()

# Configuração da tela do Pygame
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption('Controle dos Servos com Mouse')

# Inicialização da webcam
cap = cv2.VideoCapture(1)  # Usa a primeira webcam encontrada

screen_x, screen_y = 0, 0
pyautogui.moveTo(screen_x + screen_width // 2, screen_y + screen_height // 2)

last_mouse_x, last_mouse_y = pygame.mouse.get_pos()
last_sent_time = time.time()

laser_on = False  # Estado inicial do lazer
laser_command = "0\n"  # Comando para desligar o lazer

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Pressionar ESC para sair
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo do mouse liga/desliga o lazer
                laser_on = not laser_on
                laser_command = "1\n" if laser_on else "0\n"

    # Captura frame da webcam
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)  # Espelha horizontalmente
        frame = cv2.resize(frame, (screen_width, screen_height))  # Redimensiona para o tamanho da tela
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para RGB (Pygame usa RGB)
        frame = np.rot90(frame)  # Rotaciona para exibição correta
        frame = pygame.surfarray.make_surface(frame)  # Converte para surface do Pygame
        screen.blit(frame, (0, 0))  # Desenha a webcam como fundo

    current_mouse_x, current_mouse_y = pygame.mouse.get_pos()

    if current_mouse_x != last_mouse_x or current_mouse_y != last_mouse_y:
        current_time = time.time()

        if current_time - last_sent_time > 0.02:
            servo_x = int(180 - (current_mouse_x / screen_width) * 180)
            servo_y = int((current_mouse_y / screen_height) * 180)

            # Envia os comandos para os servos e o lazer
            command = f"{servo_x},{servo_y},{laser_command}"
            arduino.write(command.encode('utf-8'))
            arduino.flush()

            last_sent_time = current_time
            last_mouse_x, last_mouse_y = current_mouse_x, current_mouse_y

    pyautogui.moveTo(screen_x + screen_width // 2, screen_y + screen_height // 2)

    # Desenha um indicador na posição do mouse
    pygame.draw.circle(screen, (255, 0, 0), (current_mouse_x, current_mouse_y), 10)
    pygame.display.flip()

# Fecha tudo ao sair
cap.release()
arduino.close()
pygame.quit()
