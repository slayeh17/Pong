import pygame
pygame.init()

pygame.display.set_caption("Pong")

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
DELAY = 3000
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BROWN = "#84714F"
P_WIDTH, P_HEIGHT = 20, 100
BALL_RAD = 7
SCORE_FONT = pygame.font.SysFont("arial", 50)
WIN_SCORE = 5

class Ball:
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 1

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 1

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BROWN)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i%2==0:
            pygame.draw.rect(win, WHITE, (WIDTH//2-5, i, 10, HEIGHT//20))

    ball.draw(win)

    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y+ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y-ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel <= 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y+left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1*y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y+right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1*y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y >= 0:
        left_paddle.move(True)
    if keys[pygame.K_s] and left_paddle.y+left_paddle.height <= HEIGHT:
        left_paddle.move(False)

    if keys[pygame.K_UP] and right_paddle.y >= 0:
        right_paddle.move(True)
    if keys[pygame.K_DOWN] and right_paddle.y+right_paddle.height <= HEIGHT:
        right_paddle.move(False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2-P_HEIGHT//2, P_WIDTH, P_HEIGHT)
    right_paddle = Paddle(WIDTH-10-P_WIDTH, HEIGHT//2-P_HEIGHT//2, P_WIDTH, P_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RAD)

    left_score, right_score = 0,0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        won = False
        win_text = ""
        if left_score == WIN_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score == WIN_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, BLACK)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(DELAY)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

        if ball.x < 0:
            right_score+=1
            ball.reset()
        elif ball.x > WIDTH:
            left_score+=1
            ball.reset()

    pygame.quit()

if __name__ == '__main__':
    main()