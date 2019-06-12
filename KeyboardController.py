import pygame
from Drone import Drone
from time import sleep, time
from math import sin, cos, radians
import numpy as np
from pygame.locals import *
import os


if __name__ == '__main__':
    SENSITIVITY = 0.5
    pygame.init()

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)

    width, height = 1280, 720
    center = (width // 2, height // 2)
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(640) + "," + str(360)
    pygame.display.set_caption('Parrot AR 2.0 Keyboard Controller')
    window = pygame.display.set_mode((width, height))

    # Wait for keypress to launch drone
    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render('Press enter to launch', True, white)
    textRect = text.get_rect()
    textRect.center = center
    window.blit(text, textRect)
    pygame.display.update()
    waiting = True
    while waiting:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    sleep(1)

    drone = Drone()
    drone.takeoff()

    # Window main loop
    while True:
        # Fetch current data
        try:
            data = drone.getNavData()
        except:
            print("Can't find drone")

        # Idk black screen for now since I don't have the dope 720p video feed from the drone yet
        try:
            frame = drone.frame
            window.blit(pygame.transform.flip(pygame.transform.scale(pygame.surfarray.make_surface(np.rot90(frame)), (1280, 720)), True, False), (0, 0))
        except:
            print("Can't find camera")
            window.fill(black)

        # Pitch/Roll stuff
        try:
            pitch = data.theta / 1000
            roll = data.phi / 1000
        except:
            print("Can't find gyroscope")
            pitch, roll = 0, 0
        guageCenter = (center[0], center[1])
        radius = 100  # Radius for the gap between the center of the guage and the lines
        pitchOffset = 100  # Multiplier for how aggressive the pitch offset should be
        lineLength = 100
        # This will display bars at -30, -15, 0, 15, 30 deg
        for i in range(-2, 3):
            currentLineLength = lineLength if i != 0 else lineLength + 25
            # Don't ask me how this works its a lot of math and trig and stuff to place the pretty green bars for pitch and roll
            pygame.draw.line(window, green, (int(guageCenter[0] - radius * cos(radians(roll)) - pitchOffset * i * sin(radians(roll))), int((guageCenter[1] - radius * sin(radians(roll))) + pitchOffset * i * cos(radians(roll)) + pitchOffset * 4 * sin(radians(pitch)))),
                                            (int(guageCenter[0] - (radius + currentLineLength) * cos(radians(roll)) - pitchOffset * i * sin(radians(roll))), int(guageCenter[1] - (radius + currentLineLength) * sin(radians(roll)) + pitchOffset * i * cos(radians(roll)) + pitchOffset * 4 * sin(radians(pitch)))))
            pygame.draw.line(window, green, (int(guageCenter[0] + radius * cos(radians(roll)) - pitchOffset * i * sin(radians(roll))), int((guageCenter[1] + radius * sin(radians(roll))) + pitchOffset * i * cos(radians(roll)) + pitchOffset * 4 * sin(radians(pitch)))),
                                            (int(guageCenter[0] + (radius + currentLineLength) * cos(radians(roll)) - pitchOffset * i * sin(radians(roll))), int(guageCenter[1] + (radius + currentLineLength) * sin(radians(roll)) + pitchOffset * i * cos(radians(roll)) + pitchOffset * 4 * sin(radians(pitch)))))

        # Center reticle
        pygame.draw.line(window, green, (center[0] - 25, center[1]), (center[0] - radius + 25, center[1]))
        pygame.draw.line(window, green, (center[0] - 25, center[1]), (center[0], center[1] + 25))
        pygame.draw.line(window, green, (center[0] + 25, center[1]), (center[0], center[1] + 25))
        pygame.draw.line(window, green, (center[0] + 25, center[1]), (center[0] + radius - 25, center[1]))

        # Battery
        batteryColor = red
        try:
            batteryPercentage = int(data.vbat_flying_percentage)
            if batteryPercentage > 33:
                batteryColor = yellow
            if batteryPercentage > 66:
                batteryColor = green
        except:
            print("Can't find battery percentage")
            batteryPercentage = 'N/A'
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Batt:{}%'.format(batteryPercentage), True, batteryColor)
        textRect = text.get_rect()
        textRect.center = (width - 55, 20)
        window.blit(text, textRect)

        # Altitude
        try:
            altitude = 100 * data.altitude
        except:
            print("Can't find ultrasonic sensor")
            altitude = 10
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('{}m'.format(altitude), True, green)
        textRect = text.get_rect()
        textRect.center = (width - 30, height - (10 * altitude) - 11)
        window.blit(text, textRect)
        text = font.render('ALT', True, green)
        textRect = text.get_rect()
        textRect.center = (width - 30, height - (10 * altitude) - 32)
        window.blit(text, textRect)
        pygame.draw.rect(window, green, (width - 50, height - (10 * altitude), 40, height - (10 * altitude)))

        # Boring quit button stuff
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Keypresses for movement
        keys = pygame.key.get_pressed()
        # Forward
        if keys[pygame.K_w]:
            print('forward')
            drone.move(forward=SENSITIVITY)
        # Backward
        if keys[pygame.K_s]:
            print('backward')
            drone.move(backward=SENSITIVITY)
        # Left
        if keys[pygame.K_a]:
            print('left')
            drone.move(left=SENSITIVITY)
        # Right
        if keys[pygame.K_d]:
            print('right')
            drone.move(right=SENSITIVITY)
        # Up
        if keys[pygame.K_UP]:
            print('up')
            drone.move(up=SENSITIVITY)
        # Down
        if keys[pygame.K_DOWN]:
            print('down')
            drone.move(down=SENSITIVITY)
        # Rotate Clockwise
        if keys[pygame.K_RIGHT]:
            print('clockwise')
            drone.move(cw=SENSITIVITY)
        # Rotate Counterclockwise
        if keys[pygame.K_LEFT]:
            print('counterclockwise')
            drone.move(ccw=SENSITIVITY)
        # Land/Takeoff
        if keys[pygame.K_SPACE]:
            if drone.isFlying():
                drone.land()
            else:
                drone.takeoff()
            sleep(1)

        pygame.display.update()
