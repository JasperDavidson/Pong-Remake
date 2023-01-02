import pygame
from pygame.locals import *

class GameObject:

    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height
        self.pos = image.get_rect().move(0, height)


class Paddle(GameObject):

    def __init__(self, image, width, height, screen_width, screen_height, speed, number):
        super().__init__(image, width, height)
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.moving = False
        self.up = False

        if number % 2 == 0:
            self.pos = image.get_rect().move(screen_width - width, height)

    def move(self, up=False, down=False):
        if up:
            self.pos.top -= self.speed
            self.moving = True
            self.up = True
        if down:
            self.pos.top += self.speed
            self.moving = True


class Ball(GameObject):

    def __init__(self, image, width, height, screen_width, screen_height, speed):
        super().__init__(image, width, height)
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dx = speed
        self.dy = 0
        self.pos = image.get_rect().move(screen_width // 2, screen_height // 2)

    def collision(self, left_paddle, right_paddle, left_moving, right_moving, left_up, right_up, paddle_speed):
        if self.pos.top <= 0:
            self.dy *= -1
        if self.pos.bottom >= self.screen_height:
            self.dy *= -1

        if self.dx < 0 and self.pos.colliderect(left_paddle):
            if left_moving and left_up:
                self.dy -= paddle_speed // 3
                self.dx *= -1
            elif left_moving:
                self.dy += paddle_speed // 3
                self.dx *= -1
            else:
                self.dx *= -1

        if self.dx > 0 and self.pos.colliderect(right_paddle):
            if right_moving and right_up:
                self.dy -= paddle_speed // 3
                self.dx *= -1
            elif right_moving:
                self.dy += paddle_speed // 3
                self.dx *= -1
            else:
                self.dx *= -1

    def move(self):
        self.pos.left += self.dx
        self.pos.top += self.dy
