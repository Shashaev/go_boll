import pygame
from math import acos, pi, tan
from PIL import Image, ImageDraw


class Bol:
    def __init__(self, x0: float, y0: float, radius: float, direction: list[float, float]):
        self.x0, self.y0 = x0, y0
        self.r = radius
        self.x, self.y = direction
        self.speed = (self.x ** 2 + self.y ** 2) ** 0.5

        if self.speed == 0:
            self.x = 0
            self.y = 0
        else:
            self.x /= self.speed
            self.y /= self.speed

    def run(self):
        self.x0 += self.x * self.speed
        self.y0 += self.y * self.speed

        x1, y1 = 0, 0

        if (self.x0 + self.r) >= size[0]:
            self.x0 -= self.x0 + self.r - size[0]
            x1 -= 1
        elif (self.x0 - self.r) <= 0:
            self.x0 += abs(self.x0 - self.r)
            x1 += 1
        elif (self.y0 + self.r) >= size[1]:
            self.y0 -= self.y0 + self.r - size[1]
            y1 -= 1
        elif (self.y0 - self.r) <= 0:
            self.y0 += abs(self.y0 - self.r)
            y1 += 1
        else:
            return True

        cs = (-self.x * x1 + -self.y * y1) / (self.x ** 2 + self.y ** 2) ** 0.5
        ar = pi / 2 - acos(cs)

        if x1 == 0:
            if self.x != 0:
                self.x = (1 / tan(ar)) * self.x / abs(self.x)
            else:
                self.x = 0
        else:
            self.x = x1

        if y1 == 0:
            if self.y != 0:
                self.y = (1 / tan(ar)) * self.y / abs(self.y)
            else:
                self.y = 0
        else:
            self.y = y1

        s = (self.x ** 2 + self.y ** 2) ** 0.5

        if s != 0:
            self.x /= s
            self.y /= s
        else:
            self.x = 0
            self.y = 0

    def get_par(self):
        return self.x0 - self.r, self.y0 - self.r, self.x0 + self.r, self.y0 + self.r

    def get_xy(self):
        return self.x0, self.y0

    def get_radius(self):
        return self.r


def mouse_button_left():
    x, y = pygame.mouse.get_pos()
    x -= line[0]
    y -= line[1]
    x /= 100
    y /= 100

    bot = Bol(line[0], line[1], 20, [x, y])

    bots.append(bot)


def mouse_move():
    line[2], line[3] = pygame.mouse.get_pos()


def mouse_button_right():
    line[0], line[1] = pygame.mouse.get_pos()


def main_loop():
    clock = pygame.time.Clock()

    while True:

        for even in pygame.event.get():
            if even.type == pygame.MOUSEBUTTONUP:
                if even.button == 1:
                    mouse_button_left()
                elif even.button == 3:
                    mouse_button_right()
            elif even.type == pygame.MOUSEMOTION:
                mouse_move()
            elif even.type == pygame.QUIT:
                pygame.quit()

        screen.fill('white')
        pygame.draw.line(screen, 'red', line[0: 2], line[2: 4])

        for bot in bots:
            bot.run()

        for bot in bots:
            pygame.draw.circle(screen, 'green', bot.get_xy(), bot.get_radius())

        pygame.display.flip()
        clock.tick(100)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('go_ball')

    size = (500, 600)
    screen = pygame.display.set_mode(size)
    img = Image.new('RGB', size)
    img_dr = ImageDraw.ImageDraw(img)
    bots = []
    line = [size[0] / 2, size[1] / 2, 0, 0]
    main_loop()
