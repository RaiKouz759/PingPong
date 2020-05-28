import pygame
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 220, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (220, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 220)
BRIGHT_BLUE = (0, 0, 255)
BALL_SIZE = 10
BALL_SPEED = 5
DEFLECTOR_SPEED = 5
DASH_SPEED = 10
DEFLECTOR_LENGTH = 80
DEFLECTOR_WIDTH = 9
count = 0

pygame.init()
game_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
deflector_sprites = [pygame.image.load('deflector.png').convert(), pygame.image.load('deflector_half.png').convert(), pygame.image.load('deflector3.png').convert(), pygame.image.load('deflector4.png').convert()]
deflectorImg = pygame.image.load('deflector.png')
clock = pygame.time.Clock()


class Ball:

    def __init__(self, color, x, y, x_speed, y_speed):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.color = color

    def move(self, deflec_pos, deflec_oppo_pos, deflec_speed, deflec_oppo_speed):
        if self.x + self.x_speed >= SCREEN_WIDTH or self.x + self.x_speed <= 0:
            self.x_speed = self.x_speed * -1

        if (deflec_pos[1] + DEFLECTOR_WIDTH > self.y > deflec_pos[1]
                and deflec_pos[0] < self.x < deflec_pos[0] + DEFLECTOR_LENGTH):
            self.y_speed = self.y_speed * -1
            self.x_speed += int(0.5 * deflec_speed)

        if deflec_oppo_pos[1] < self.y + self.y_speed < deflec_oppo_pos[1] + DEFLECTOR_WIDTH \
                and deflec_oppo_pos[0] < self.x < deflec_oppo_pos[0] + DEFLECTOR_LENGTH:
            self.y_speed = self.y_speed * -1
            self.x_speed += int(0.5 * deflec_oppo_speed)

        self.x += self.x_speed
        self.y += self.y_speed

    def reset(self):
        self.x = int(SCREEN_WIDTH * 0.5)
        self.y = int(SCREEN_HEIGHT * 0.5)
        self.y_speed = BALL_SPEED
        self.x_speed = 0

    def score(self):

        if self.y + self.y_speed > SCREEN_HEIGHT:
            return 1
        elif self.y + self.y_speed < 0:
            return 0
        return -1

    def draw(self):
        pygame.draw.circle(game_display, self.color, (self.x, self.y), BALL_SIZE)


class Deflector:

    def __init__(self, x, y, x_speed, orientation):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.image = pygame.image.load('deflector.png')
        self.orientation = orientation  # 0 is top, 1 is bottom of screen
        self.pos_buffer = [0, 0, 0, 0]
        self.dashing = 0

    def move(self):
        global count
        if 0 <= self.x + self.x_speed <= SCREEN_WIDTH - DEFLECTOR_LENGTH:
            self.x += self.x_speed
            if count % 5 == 0:
                self.pos_buffer.pop()
                self.pos_buffer.insert(0, self.x)

    def set_speed(self, speed):
        self.x_speed = speed

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def get_speed(self):
        return self.x_speed

    def set_dash(self, s):
        if s == 1:
            self.dashing = 1
        else:
            self.dashing = 0

    def draw(self):
        # for i in range(len(self.pos_buffer)):
        #     game_display.blit(deflector_sprites[3-i], (self.pos_buffer[3-i], self.y))
        # The for loop is much slower than just writing out the expressions.
        if self.dashing == 1:
            game_display.blit(deflector_sprites[3], (self.pos_buffer[3], self.y))
            game_display.blit(deflector_sprites[2], (self.pos_buffer[2], self.y))
            game_display.blit(deflector_sprites[1], (self.pos_buffer[1], self.y))
        game_display.blit(deflector_sprites[0], (self.x, self.y))

    def reset(self):
        if self.orientation:
            self.set_pos(int(0.45 * SCREEN_WIDTH), int(0.9 * SCREEN_HEIGHT))
        else:
            self.set_pos(int(0.45 * SCREEN_WIDTH), int(0.1 * SCREEN_HEIGHT))
        self.set_speed(0)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, size, x, y, color):
    """Displays text on surface game_display"""

    fontText = pygame.font.Font('freesansbold.ttf', size)
    textSurf = fontText.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    game_display.blit(textSurf, textRect)


def dash_key_activated(key_input_buffer, key):
    '''

    :param key_input_buffer: array for storing past times of key inputs
    :param key: key that was pressed
    :return:
    '''

    time = pygame.time.get_ticks()
    time_dif = time - key_input_buffer[key]
    key_input_buffer[key] = time

    if time_dif < 300:
        print("DASH ACTIVATED")
        return True
    else:
        return False


def game_loop():
    x = (SCREEN_WIDTH * 0.45)
    y = (SCREEN_HEIGHT * 0.9)
    y_oppo = (SCREEN_HEIGHT * 0.1)
    deflector = Deflector(x, y, 0, 1)
    deflector_opponent = Deflector(x, y_oppo, 0, 0)
    ball = Ball(RED, int(0.5*SCREEN_WIDTH), int(SCREEN_HEIGHT / 2), 0, 5)
    current_direction = 0  # 1 is to the right, -1 is to the left
    current_direction_oppo = 0
    score = [0, 0]
    key_input_buffer = [0, 0, 0, 0]
    global count

    round = 1
    while True:

        for event in pygame.event.get():
            print(key_input_buffer)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if dash_key_activated(key_input_buffer, 0):
                        deflector.set_dash(1)
                        deflector.set_speed(DASH_SPEED)
                    else:
                        deflector.set_dash(0)
                        deflector.set_speed(DEFLECTOR_SPEED)
                    current_direction = pygame.K_RIGHT

                if event.key == pygame.K_d:
                    if dash_key_activated(key_input_buffer, 1):
                        deflector_opponent.set_dash(1)
                        deflector_opponent.set_speed(DASH_SPEED)
                    else:
                        deflector_opponent.set_dash(0)
                        deflector_opponent.set_speed(DEFLECTOR_SPEED)
                    current_direction_oppo = pygame.K_d

                if event.key == pygame.K_LEFT:
                    if dash_key_activated(key_input_buffer, 2):
                        deflector.set_dash(1)
                        deflector.set_speed(DASH_SPEED * -1)
                    else:
                        deflector.set_dash(0)
                        deflector.set_speed(DEFLECTOR_SPEED * -1)
                    current_direction = pygame.K_LEFT

                if event.key == pygame.K_a:
                    if dash_key_activated(key_input_buffer, 3):
                        deflector_opponent.set_dash(1)
                        deflector_opponent.set_speed(DASH_SPEED * -1)
                    else:
                        deflector_opponent.set_dash(0)
                        deflector_opponent.set_speed(DEFLECTOR_SPEED * -1)
                    current_direction_oppo = pygame.K_a

            if event.type == pygame.KEYUP and event.key == current_direction:
                deflector.set_speed(0)

            if event.type == pygame.KEYUP and event.key == current_direction_oppo:
                deflector_opponent.set_speed(0)

        deflector.move()
        deflector_opponent.move()
        ball.move(deflector.get_pos(), deflector_opponent.get_pos(), deflector.get_speed(),
                  deflector_opponent.get_speed())
        game_display.fill(WHITE)
        deflector.draw()
        deflector_opponent.draw()
        ball.draw()

        if ball.score() != -1:
            score[ball.score()] += 1
            deflector_opponent.reset()
            deflector.reset()
            ball.reset()

        message_display("Score: %d" % score[1], 30, 0.9 * SCREEN_WIDTH, 0.1 * SCREEN_HEIGHT, BLACK)
        message_display("Score: %d" % score[0], 30, 0.9 * SCREEN_WIDTH, 0.9 * SCREEN_HEIGHT, BLACK)
        count += 1
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
