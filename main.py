import pygame, sys
import PongClasses
from pygame.locals import *
pygame.init()


def start_screen(screen, font):
    icon = pygame.image.load("communityIcon_acwnxauia1p01.png").convert()
    pygame.display.set_caption("Pong")
    pygame.display.set_icon(icon)

    text_welcome = font.render("Welcome to Pong!", True, (255, 255, 255))
    text_play = font.render("Play", True, (255, 255, 255))
    text_skins = font.render("Skins", True, (255, 255, 255))
    text_rect_welcome = text_welcome.get_rect()
    text_rect_play = text_play.get_rect()
    text_rect_skins = text_skins.get_rect()

    text_rect_welcome.centerx = screen.get_rect().centerx
    text_rect_welcome.centery = screen.get_rect().centery

    text_rect_play.centerx = screen.get_rect().centerx - 100
    text_rect_play.centery = screen.get_rect().centery + 100

    text_rect_skins.centerx = screen.get_rect().centerx + 100
    text_rect_skins.centery =  screen.get_rect().centery + 100

    screen.blit(text_welcome, text_rect_welcome)
    screen.blit(text_play, text_rect_play)
    screen.blit(text_skins, text_rect_skins)
    pygame.draw.rect(screen, (255, 0, 0), text_rect_play, 3)
    pygame.draw.rect(screen, (0, 255, 0), text_rect_skins, 3)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if text_rect_play.collidepoint(event.pos):
                        return 1
                    if text_rect_skins.collidepoint(event.pos):
                        return 2


def skins(screen):
    screen.fill((0, 0, 0))

    text_fire_ball = font.render("Fire Ball", True, (255, 255, 255))
    text_moss_ball = font.render("Moss Ball", True, (255, 255, 255))
    text_water_ball = font.render("Water Ball", True, (255, 255, 255))
    text_rect_fire_ball = text_fire_ball.get_rect()
    text_rect_moss_ball = text_moss_ball.get_rect()
    text_rect_water_ball = text_water_ball.get_rect()

    text_rect_water_ball.centerx = screen.get_rect().centerx
    text_rect_water_ball.centery = screen.get_rect().centery

    text_rect_fire_ball.centerx = screen.get_rect().centerx
    text_rect_fire_ball.centery = screen.get_rect().centery - 200

    text_rect_moss_ball.centerx = screen.get_rect().centerx
    text_rect_moss_ball.centery = screen.get_rect().centery + 200

    screen.blit(text_fire_ball, text_rect_fire_ball)
    screen.blit(text_water_ball, text_rect_water_ball)
    screen.blit(text_moss_ball, text_rect_moss_ball)

    pygame.draw.rect(screen, (255, 0, 0), text_rect_fire_ball, 4)
    pygame.draw.rect(screen, (0, 0, 255), text_rect_water_ball, 4)
    pygame.draw.rect(screen, (0, 255, 0), text_rect_moss_ball, 4)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if text_rect_fire_ball.collidepoint(event.pos):
                        return 1
                    if text_rect_water_ball.collidepoint(event.pos):
                        return 2
                    if text_rect_moss_ball.collidepoint(event.pos):
                        return 3


def main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path):
    paddle_width = 30
    paddle_height = 200
    ball_width = 20
    ball_height = 20
    fps = 60
    game_over = False

    paddle_speed = 7
    ball_speed = 9
    clock = pygame.time.Clock()

    paddle_image = pygame.transform.scale(pygame.image.load("pixil-frame-0(2).png").convert(), (paddle_width, paddle_height))
    ball_image = pygame.transform.scale(pygame.image.load(ball_image_path).convert(), (ball_width, ball_height))
    paddle_one = PyGameExperiments.Paddle(paddle_image, paddle_width, paddle_height, screen_width, screen_height,
                                          paddle_speed, 1)
    paddle_two = PyGameExperiments.Paddle(paddle_image, paddle_width, paddle_height, screen_width, screen_height,
                                          paddle_speed, 2)
    ball = PyGameExperiments.Ball(ball_image, ball_width, ball_height, screen_width, screen_height, ball_speed)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            paddle_two.move(up=True)
        if keys[pygame.K_DOWN]:
            paddle_two.move(down=True)
        if keys[pygame.K_w]:
            paddle_one.move(up=True)
        if keys[pygame.K_s]:
            paddle_one.move(down=True)
        if keys[pygame.K_r]:
            main(screen, screen_width, screen_height, left_score, right_score, ball_image_path)

        ball.collision(paddle_one.pos, paddle_two.pos, paddle_one.moving, paddle_two.moving, paddle_one.up, paddle_two.up, paddle_speed)
        ball.move()

        if ball.pos.colliderect(screen.get_rect().left, 0, 1, screen.get_rect().height):
            left_score += 1
            main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path)

        if ball.pos.colliderect(screen.get_rect().right, 0, 1, screen.get_rect().height):
            right_score += 1
            main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path)

        paddle_one.pos.clamp_ip(screen.get_rect())
        paddle_two.pos.clamp_ip(screen.get_rect())
        ball.pos.clamp_ip(screen.get_rect())

        screen.blit(paddle_one.image, paddle_one.pos)
        screen.blit(paddle_two.image, paddle_two.pos)
        screen.blit(ball.image, ball.pos)

        pygame.draw.line(screen, (255, 255, 255), (screen_width // 2, 0), (screen_width // 2, screen_height), 5)

        text_left_score = font.render(str(left_score), True, (255, 255, 255))
        text_rect_left_score = text_left_score.get_rect()
        text_rect_left_score.centerx = (screen.get_rect().centerx // 2) * 3
        text_rect_left_score.centery = screen.get_rect().centery // 2
        screen.blit(text_left_score, text_rect_left_score)

        text_right_score = font.render(str(right_score), True, (255, 255, 255))
        text_rect_right_score = text_right_score.get_rect()
        text_rect_right_score.centerx = screen.get_rect().centerx // 2
        text_rect_right_score.centery = screen.get_rect().centery // 2
        screen.blit(text_right_score, text_rect_right_score)

        if left_score == 5 or right_score == 5:
            game_over = True

        clock.tick(fps)
        pygame.display.flip()

    screen.fill((0, 0, 0))

    text_over = font.render("Game Over", True, (255, 255, 255))
    text_retry = font.render("Retry", True, (255, 255, 255))
    text_rect_over = text_over.get_rect()
    text_rect_retry = text_retry.get_rect()

    text_rect_over.centerx = screen.get_rect().centerx
    text_rect_over.centery = screen.get_rect().centery

    text_rect_retry.centerx = text_rect_over.centerx
    text_rect_retry.centery = screen.get_rect().centery + 100

    screen.blit(text_over, text_rect_over)
    screen.blit(text_retry, text_rect_retry)
    pygame.draw.rect(screen, (255, 0, 0), text_rect_retry, 3)
    pygame.display.flip()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if text_rect_retry.collidepoint(event.pos):
                        left_score, right_score = 0, 0
                        main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path)


screen_width = 1000
screen_height = 800
left_score, right_score = 0, 0
font = pygame.font.Font(None, 100)
ball_image_path = "pixil-frame-0(2).png"
screen = pygame.display.set_mode((screen_width, screen_height))
start_value = start_screen(screen, font)
skins_value = skins(screen)


if start_value == 1:
    main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path)
elif start_value == 2:
    if skins_value == 1:
        ball_image_path = "pixil-frame-0(3).png"
        main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path)
    if skins_value == 2:
        ball_image_path = "pixil-frame-0(4).png"
        main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path)
    if skins_value == 3:
        ball_image_path = "pixil-frame-0(5).png"
        main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path)
