# examples/game_snake.py: version: 2020-10-18 02:00
#
# Snake game example
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/game_snake.py
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> import examples.game_snake as eg
# >>> from examples.game_snake import run
# >>> run()
#
# To Do
# ~~~~~
# - Python snake graphic bitmap !
# - Single player solitaire
# - Single player versus computer
# - Multi-player snake: Latency issues ?
# - Score and snake tail increases when food eaten

import uos

import aiko.event as event
import aiko.oled as oled

oled0 = oled.oleds[0]  # Game screen
oled1 = oled.oleds[1]  # Score, status, instructions, diagnostics

offset = oled.font_size
height = oled0.height - offset
width = oled0.width

allowed_headings = [(-1, 0), (1, 0), (0, -1), (0, 1)]

score = 0
snake_heading = None         # (delta_x, delta_y)
snake_heading_change = None  # frame count
snake_position = None        # (x, y)

def display_score():
    global score
    oled1.fill_rect(0, offset + oled.font_size, 32, oled.font_size, 0)
    oled1.text(str(score), 0, offset + oled.font_size)
    oled1.show()
    score += 1

def display_snake():
    oled0.pixel(snake_position[0], snake_position[1] + offset, 1)
    oled0.show()

def display_snake_dead():
    oled1.text("OUCH !", 0, offset + 3 * oled.font_size)
    oled1.show()
    print("Snake dead !")
    event.terminate()

def position_check(position):
    position_okay = True
    if position[0] < 0 or position[0] >= width:
        position_okay = False
    if position[1] < 0 or position[1] >= height:
        position_okay = False
    if oled0.pixel(position[0], position[1] + offset):
        position_okay = False
    return position_okay

def random(min, max, r_max=255):
    r = uos.urandom(1)[0] & r_max
    r = r / r_max * (max - min) + min
    if r >= max:
        r = min
    return int(r)

def random_position(limit):
    limit = limit // 4
    return random(limit, limit * 3)

def snake_new():
    global score, snake_heading, snake_heading_change, snake_position
    score = 0
    snake_position = (random_position(width), random_position(height))
    snake_heading, snake_heading_change = snake_new_heading()

def snake_new_heading():
    viable_headings = []
    for heading in allowed_headings:
        future_position = tuple(map(sum, zip(snake_position, heading)))
        if position_check(future_position):
            viable_headings.append(heading)
    if len(viable_headings):
        snake_heading = viable_headings[random(0, len(viable_headings))]
    else:
        snake_heading = (0, 0)
        display_snake_dead()
    snake_heading_change = random(4, 16)
    return snake_heading, snake_heading_change

def snake_update():
    global snake_heading, snake_heading_change, snake_position
    print("sp: " + str(snake_position) + ", sh: " + str(snake_heading) + ", shc: " + str(snake_heading_change))
    snake_position = tuple(map(sum, zip(snake_position, snake_heading)))
    if not position_check(snake_position):
        snake_heading = (0, 0)
        display_snake_dead()
    display_snake()
    snake_heading_change -= 1
    if snake_heading_change == 0:
        snake_heading, snake_heading_change = snake_new_heading()

def timer_handler():
    snake_update()
    display_score()

def run(period=50):
    oled.title = "Snake 0.0"
    oled.oleds_clear(0)
    snake_new()
    display_snake()

    event.add_timer_handler(timer_handler, period)
    try:
        event.loop()
    finally:
        event.remove_timer_handler(timer_handler)
