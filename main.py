import pygame, sys, random
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
    center_x = screen.get_rect().centerx
    center_y = screen.get_rect().centery

    text_rect_welcome.centerx = center_x
    text_rect_welcome.centery = center_y

    text_rect_play.centerx = center_x - 100
    text_rect_play.centery = center_y + 100

    text_rect_skins.centerx = center_x + 100
    text_rect_skins.centery = center_y + 100

    screen.blit(text_welcome, text_rect_welcome)
    screen.blit(text_play, text_rect_play)
    screen.blit(text_skins, text_rect_skins)
    pygame.draw.rect(screen, (255, 0, 0), text_rect_play, 3)
    pygame.draw.rect(screen, (0, 255, 0), text_rect_skins, 3)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if text_rect_play.collidepoint(event.pos):
                        return mode_checker(screen, font)

                    if text_rect_skins.collidepoint(event.pos):
                        return 2


def skins(screen, font, home_image_path):
    screen.fill((0, 0, 0))
    home_image = pygame.image.load("pixil-frame-0(6).png").convert()
    home_image_rect = home_image.get_rect()

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
    screen.blit(home_image, home_image_rect)

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
                        return 1, mode_checker(screen, font)
                    if text_rect_water_ball.collidepoint(event.pos):
                        return 2, mode_checker(screen, font)
                    if text_rect_moss_ball.collidepoint(event.pos):
                        return 3, mode_checker(screen, font)
                    if home_image_rect.collidepoint(event.pos):
                        return 4, mode_checker(screen, font)


def mode_checker(screen, font):
    text_powerup = font.render("Powerup Mode", True, (255, 255, 255))
    text_normal = font.render("Normal Mode", True, (255, 255, 255))
    text_rect_powerup = text_powerup.get_rect()
    text_rect_normal = text_normal.get_rect()

    text_rect_powerup.centerx = screen.get_rect().centerx
    text_rect_powerup.centery = screen.get_rect().centery + 100
    text_rect_normal.centerx = screen.get_rect().centerx
    text_rect_normal.centery = screen.get_rect().centery - 100

    screen.fill((0, 0, 0))
    screen.blit(text_normal, text_rect_normal)
    screen.blit(text_powerup, text_rect_powerup)
    pygame.draw.rect(screen, (128, 128, 0), text_rect_normal, 3)
    pygame.draw.rect(screen, (0, 128, 128), text_rect_powerup, 3)

    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if text_rect_normal.collidepoint(event.pos):
                        return 0
                    if text_rect_powerup.collidepoint(event.pos):
                        return 1


def powerup(ball, timer, fps, random_powerup, time_delay, speed_powerup, slow_powerup, expand_powerup, last_paddle):
    powerup_timer = timer

    if powerup_timer == fps * time_delay:
        if random_powerup == 1:
            if ball.pos.colliderect(speed_powerup.pos):
                speed_powerup.effect(ball)
                return 0
            screen.blit(speed_powerup.image, speed_powerup.pos)
            return fps * time_delay
        elif random_powerup == 2:
            if ball.pos.colliderect(slow_powerup.pos):
                slow_powerup.effect(ball)
                return 0
            screen.blit(slow_powerup.image, slow_powerup.pos)
            return fps * time_delay
        elif random_powerup == 3:
            if ball.pos.colliderect(expand_powerup.pos):
                expand_powerup.effect(last_paddle)
                return 0
            screen.blit(expand_powerup.image, expand_powerup.pos)
            return fps * time_delay

    else:
        powerup_timer += 1
        return powerup_timer


def main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode):
    paddle_width = 30
    paddle_height = 200
    ball_width = 20
    ball_height = 20
    powerup_width = 40
    powerup_height = 40
    fps = 60
    paddle_speed = 8
    ball_speed = 9
    time_delay = 5
    speed_powerup_increase = 2
    slow_powerup_decrease = 1
    expand_powerup_height_increase = 100
    random_powerup = random.randint(1, 3)
    power_timer = 1
    main_timer = 0
    win_score = 5
    ball_collision_value = "right"
    game_over = False
    clock = pygame.time.Clock()

    home_image = pygame.image.load(home_image_path).convert()
    home_image_rect = home_image.get_rect()
    paddle_image = pygame.transform.scale(pygame.image.load("pixil-frame-0(2).png").convert(), (paddle_width, paddle_height))
    ball_image = pygame.transform.scale(pygame.image.load(ball_image_path).convert(), (ball_width, ball_height))

    speed_powerup_image = pygame.image.load("pixil-frame-0(7).png").convert()
    speed_powerup = PongClasses.SpeedPowerup(speed_powerup_image, powerup_width, powerup_height, screen_width, screen_height, speed_powerup_increase)
    slow_powerup_image = pygame.image.load("pixil-frame-0(8).png").convert()
    slow_powerup = PongClasses.SlowPowerup(slow_powerup_image, powerup_width, powerup_height, screen_width, screen_height, slow_powerup_decrease)
    expand_powerup_image = pygame.image.load("pixil-frame-0(9).png").convert()
    expand_powerup = PongClasses.ExpandPowerup(expand_powerup_image, powerup_width, powerup_height, screen_width, screen_height, expand_powerup_height_increase)

    paddle_one = PongClasses.Paddle(paddle_image, paddle_width, paddle_height, screen_width, screen_height, paddle_speed, 1)
    paddle_two = PongClasses.Paddle(paddle_image, paddle_width, paddle_height, screen_width, screen_height, paddle_speed, 2)
    ball = PongClasses.Ball(ball_image, ball_width, ball_height, screen_width, screen_height, ball_speed)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if home_image_rect.collidepoint(event.pos):
                        screen.fill((0, 0, 0))
                        program_begin(ball_image_path, home_image_path)

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
            main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode)

        if ball_collision_value == "left" or ball_collision_value == "right":
            if ball_collision_value == "left":
                last_paddle = paddle_one
            else:
                last_paddle = paddle_two

        if mode == 1:
            if power_timer == fps * time_delay:
                power_timer = powerup(ball, main_timer, fps, random_powerup, time_delay, speed_powerup, slow_powerup, expand_powerup, last_paddle)
            if power_timer == 0:
                main_timer = 0
            if power_timer != fps * time_delay:
                power_timer = powerup(ball, main_timer, fps, random_powerup, time_delay, speed_powerup, slow_powerup, expand_powerup, last_paddle)
                main_timer += 1
                random_powerup = random.randint(1, 3)

        ball_collision_value = ball.collision(paddle_one.pos, paddle_two.pos, paddle_one.moving, paddle_two.moving, paddle_one.up, paddle_two.up, paddle_speed)
        ball.move()

        if ball.pos.colliderect(screen.get_rect().left, 0, 1, screen.get_rect().height):
            left_score += 1
            main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode)

        if ball.pos.colliderect(screen.get_rect().right, 0, 1, screen.get_rect().height):
            right_score += 1
            main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode)

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

        if left_score == win_score or right_score == win_score:
            game_over = True

        screen.blit(home_image, home_image_rect)

        clock.tick(fps)
        pygame.display.flip()

    screen.fill((0, 0, 0))

    if left_score == win_score:
        text_over = font.render("Player Two Wins!", True, (255, 255, 255))
    elif right_score == win_score:
        text_over = font.render("Player One Wins!", True, (255, 255, 255))

    text_retry = font.render("Retry", True, (255, 255, 255))
    text_rect_over = text_over.get_rect()
    text_rect_retry = text_retry.get_rect()

    text_rect_over.centerx = screen.get_rect().centerx
    text_rect_over.centery = screen.get_rect().centery

    text_rect_retry.centerx = text_rect_over.centerx
    text_rect_retry.centery = screen.get_rect().centery + 100

    screen.blit(text_over, text_rect_over)
    screen.blit(text_retry, text_rect_retry)
    screen.blit(home_image, home_image_rect)
    pygame.draw.rect(screen, (255, 0, 0), text_rect_retry, 3)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if text_rect_retry.collidepoint(event.pos):
                        left_score, right_score = 0, 0
                        main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode)
                    if home_image_rect.collidepoint(event.pos):
                        screen.fill((0, 0, 0))
                        program_begin(ball_image_path, home_image_path)


def program_begin(ball_image_path, home_image_path):
    start_value = start_screen(screen, font)
    while True:
        if start_value == 0:
            main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, start_value)
        if start_value == 1:
            main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, start_value)
        elif start_value == 2:
            skins_value, mode = skins(screen, font, home_image_path)
            if skins_value == 1:
                ball_image_path = "pixil-frame-0(3).png"
                main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode)
            if skins_value == 2:
                ball_image_path = "pixil-frame-0(4).png"
                main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode)
            if skins_value == 3:
                ball_image_path = "pixil-frame-0(5).png"
                main(screen, screen_width, screen_height, left_score, right_score, font, ball_image_path, home_image_path, mode)
            if skins_value == 4:
                screen.fill((0, 0, 0))
                start_value = start_screen(screen, font)


screen_width = 1000
screen_height = 800
left_score, right_score = 0, 0
font = pygame.font.Font(None, 100)
ball_image_path = "pixil-frame-0(2).png"
home_image_path = "pixil-frame-0(6).png"
screen = pygame.display.set_mode((screen_width, screen_height))

program_begin(ball_image_path, home_image_path)
