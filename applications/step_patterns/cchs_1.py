red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
black  = (  0,   0,   0)
orange = (255, 220,   0)
white  = (255, 255, 255)

leds_per_layer = 8

layer_1 = 0

colors = [
  red,
  white,
  orange,
  blue
]

color_red    = 0
color_white  = 1
color_orange = 2
color_blue   = 3

steps = [
  [ [ layer_1, layer_1, color_red,    color_red ] ],
  [ [ layer_1, layer_1, color_white,  color_white ] ],
  [ [ layer_1, layer_1, color_orange, color_orange ] ],
  [ [ layer_1, layer_1, color_blue,   color_blue ] ]
]

step_speed = 1000
