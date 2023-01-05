import pygame, random
from pygame.locals import *

class GameObject:

    def __init__(self, image, width, height, screen_width, screen_height):
        self.image = image
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pos = image.get_rect().move(0, height)


class Paddle(GameObject):

    def __init__(self, image, width, height, screen_width, screen_height, speed, number):
        super().__init__(image, width, height, screen_width, screen_height)
        self.speed = speed
        self.moving = False
        self.up = False
        self.height = height
        self.width = width
        self.number = number

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
        super().__init__(image, width, height, screen_width, screen_height)
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
                return "left"
            elif left_moving:
                self.dy += paddle_speed // 3
                self.dx *= -1
                return "left"
            else:
                self.dx *= -1
                return "left"

        if self.dx > 0 and self.pos.colliderect(right_paddle):
            if right_moving and right_up:
                self.dy -= paddle_speed // 2
                self.dx *= -1
                return "right"
            elif right_moving:
                self.dy += paddle_speed // 2
                self.dx *= -1
                return "right"
            else:
                self.dx *= -1
                return "right"

    def move(self):
        self.pos.left += self.dx
        self.pos.top += self.dy


class SpeedPowerup(GameObject):

    def __init__(self, image, width, height, screen_width, screen_height, speed_increase):
        super().__init__(image, width, height, screen_width, screen_height)
        self.speed_increase = speed_increase
        self.x = random.randint(75, screen_width - 100)
        self.y = random.randint(75, screen_height - 100)
        self.pos = image.get_rect().move(self.x, self.y)
        self.image = image

    def effect(self, ball):
        self.x = random.randint(75, self.screen_width - 100)
        self.y = random.randint(75, self.screen_height - 100)

        if ball.dx <= 0:
            ball.dx -= self.speed_increase
            self.pos = self.image.get_rect().move(self.x, self.y)
        else:
            ball.dx += self.speed_increase
            self.pos = self.image.get_rect().move(self.x, self.y)

        if ball.dy != 0:
            if ball.dy <= 0:
                ball.dy -= self.speed_increase
            else:
                ball.dy += self.speed_increase


class SlowPowerup(GameObject):

    def __init__(self, image, width, height, screen_width, screen_height, speed_decrease):
        super().__init__(image, width, height, screen_width, screen_height)
        self.speed_decrease = speed_decrease
        self.x = random.randint(100, screen_width - 100)
        self.y = random.randint(100, screen_height - 100)
        self.pos = image.get_rect().move(self.x, self.y)
        self.image = image

    def effect(self, ball):
        self.x = random.randint(100, self.screen_width - 100)
        self.y = random.randint(100, self.screen_height - 100)

        if ball.dx <= 0:
            ball.dx += self.speed_decrease
        else:
            ball.dx -= self.speed_decrease

        if ball.dy <= 0:
            ball.dy += self.speed_decrease
        else:
            ball.dy -= self.speed_decrease


class ExpandPowerup(GameObject):

    def __init__(self, image, width, height, screen_width, screen_height, height_change):
        super().__init__(image, width, height, screen_width, screen_height)
        self.height_change = height_change
        self.x = random.randint(100, screen_width - 100)
        self.y = random.randint(100, screen_height - 100)
        self.pos = image.get_rect().move(self.x, self.y)
        self.image = image

    def effect(self, last_paddle):
        self.x = random.randint(100, self.screen_width - 100)
        self.y = random.randint(100, self.screen_height - 100)
        self.pos = self.image.get_rect().move(self.x, self.y)

        last_paddle.height += self.height_change
        last_paddle.image = pygame.transform.scale(last_paddle.image, (last_paddle.width, last_paddle.height))

        if last_paddle.number % 2 == 0:
            last_paddle.pos = last_paddle.image.get_rect().move(last_paddle.screen_width - last_paddle.width, last_paddle.height)
        else:
            last_paddle.pos = last_paddle.image.get_rect().move(last_paddle.width, last_paddle.height)
