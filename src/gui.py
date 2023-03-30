"""
MIT License

Copyright (c) 2023 Simon - fantomitechno

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pygame import init
from pygame.locals import K_SPACE, K_d, K_q, RESIZABLE, QUIT, VIDEORESIZE
from pygame.font import init as finit, SysFont
from pygame.display import set_mode, flip
from pygame.draw import polygon, line
from pygame.time import Clock
from pygame.event import get as get_evenet, pump
from pygame.key import get_pressed


def select() -> list:
    res = []
    while len(res) == 0:
        area = input("Area to draw = ")
        base = input("Base to draw = ")

        f = open("solutions.csv", "r")
        solutions = f.read().splitlines()
        first_line = solutions[0].split(",")
        for solution in solutions:
            if solution.startswith(area + ",=" + base + ","):
                temp = []
                for i, s in enumerate(solution.split(",=")):
                    if "aire" in first_line[i].lower():
                        n = eval(s)
                    else:
                        n = eval(s) * 20
                    temp.append(n)  # Unsecure as hell but work
                res.append(temp)
        f.close()

        print(res)
        if len(res) == 0:
            print("No solution found")

    return res


res = select()

print(res)

if len(res) == 0:
    print("No solution found")
    exit()

init()
finit()

height = 1000
width = 1000

screen = set_mode([width, height], RESIZABLE)
font = SysFont("Arial", 20)

i = 0

origin = (500, 900)


def draw():
    screen.fill((255, 255, 255))

    line(
        screen,
        (0, 0, 255),
        (origin[0] + res[i][3], origin[1] - res[i][2]),
        (origin[0] + res[i][3], origin[1]),
        1,
    )

    polygon(
        screen,
        (0, 255, 0),
        (
            origin,
            (origin[0] + res[i][1], origin[1]),
            (origin[0] + res[i][4], origin[1] - res[i][5]),
        ),
        1,
    )

    polygon(
        screen,
        (0, 255, 0),
        (
            origin,
            (origin[0] + res[i][1], origin[1]),
            (origin[0] + res[i][7], origin[1] - res[i][8]),
        ),
        1,
    )

    polygon(
        screen,
        (255, 0, 0),
        (
            origin,
            (origin[0] + res[i][1], origin[1]),
            (origin[0] + res[i][10], origin[1] - res[i][11]),
        ),
        1,
    )

    polygon(
        screen,
        (0, 0, 0),
        (
            origin,
            (origin[0] + res[i][1], origin[1]),
            (origin[0] + res[i][3], origin[1] - res[i][2]),
        ),
        1,
    )

    screen.blit(
        font.render(f"Area of full triangle: {res[i][0]}", True, (0, 0, 255)),
        (10, 10),
    )
    screen.blit(
        font.render(f"Area of left triangle: {res[i][13]}", True, (0, 0, 255)),
        (10, 30),
    )
    screen.blit(
        font.render(f"Area of right triangle: {res[i][14]}", True, (0, 0, 255)),
        (10, 50),
    )
    screen.blit(
        font.render(f"Area of middle triangle: {res[i][12]}", True, (0, 0, 255)),
        (10, 70),
    )
    screen.blit(
        font.render(f"Area of quad: {res[i][15]}", True, (0, 0, 255)),
        (10, 90),
    )

    flip()


draw()


input_repeat_time = 0

clock = Clock()
running = True
while running:
    delta_time = clock.tick(60)
    for event in get_evenet():
        if event.type == VIDEORESIZE:
            height = event.h
            width = event.w
            screen = set_mode((event.w, event.h), RESIZABLE)
            draw()
        if event.type == QUIT:
            running = False

    pressed = get_pressed()

    if pressed[K_q] and input_repeat_time < 0:
        input_repeat_time = 0.2 * 1000
        i -= 1
        if i < 0:
            i = len(res) - 1
        draw()
    if pressed[K_d] and input_repeat_time < 0:
        input_repeat_time = 0.2 * 1000
        i += 1
        if i >= len(res):
            i = 0
        draw()

    if pressed[K_SPACE] and input_repeat_time < 0:
        input_repeat_time = 0.2 * 1000
        res = select()
        i = 0
        draw()

    input_repeat_time -= delta_time
