#  Copyright (c) 2019 Diego Damasceno
#
#  This file is part of pygame-logitechG29_wheel.
#  Documentation, related files, and licensing can be found at
#
#      <https://github.com/damascenodiego/pygame-logitechG29_wheel>.


import pygame
import logitechG29_wheel
import struct
import serial

pygame.init()

ser = serial.Serial('COM4',115200)

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# window settings
size = [600, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Steering")

FPS = 10

clock = pygame.time.Clock()

# make a controller
controller = logitechG29_wheel.Controller(0)

# game logic
ball_pos1 = [100, 290]
ball_pos2 = [200, 290]
ball_pos3 = [300, 290]
ball_pos4 = [400, 290]

# game loop
done = False

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while not done:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # handle joysticks
    jsButtons = controller.get_buttons()
    jsInputs = controller.get_axis()

    steerPos = controller.get_steer()

    throtPos = controller.get_throttle()
    breakPos = controller.get_break()
    clutchPos = controller.get_clutch()

    # print(f"Throttle position {throtPos}")
    #  print(f"Brake position {breakPos}")

    throtVal = (((-1*throtPos)+1)**4)/4 + (breakPos+1)/4
    if(throtVal>1) :  throtVal = 1
    elif(throtVal<0) : throtVal = 0

    steerVal = ((steerPos+0.73)/2)
    if(steerVal>1) : steerVal=1
    elif(steerVal<0) : steerVal=0


    msg = struct.pack('ff',throtVal,steerVal)

    # msgX = bytes([126 + int(steerPos * 126)])
    # msgY = bytes([126 + int(throtPos * 126)])
    # msgZ = bytes([126 + int(breakPos * 126)])
    ser.write(msg)

    ball1_radius = int((steerPos + 1) * 20)
    ball2_radius = int((clutchPos + 1) * 20)
    ball3_radius = int((breakPos + 1) * 20)
    ball4_radius = int((throtPos + 1) * 20)

    if (steerPos >= 0):
        ball_color = RED
    else:
        ball_color = GREEN

    # drawing
    screen.fill(BLACK)
    pygame.draw.circle(screen, ball_color, ball_pos1, ball1_radius)

    pygame.draw.circle(screen, ball_color, ball_pos2, ball2_radius)

    pygame.draw.circle(screen, ball_color, ball_pos3, ball3_radius)

    pygame.draw.circle(screen, ball_color, ball_pos4, ball4_radius)

    # update screen
    pygame.display.flip()
    clock.tick(FPS)

# close window on quit
pygame.quit()