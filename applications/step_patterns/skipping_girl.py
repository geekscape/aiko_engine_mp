red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
black  = (  0,   0,   0)
orange = (255, 220,   0)
white  = (255, 255, 255)

leds_per_layer = 10

layer_rope_front         = 0
layer_rope_top           = 1
layer_main               = 2
layer_collar_socks       = 3
layer_skin_hair          = 4
layer_eyes_shoes_handles = 5
layer_rope_bottom        = 6
layer_rope_back          = 7

colors = [
  black,   # background
  red,     # main
  white,   # collar, socks
  orange,  # skin, hair
  blue,    # eyes, shoes, handles
  red      # rope
]

color_background         = 0
color_main               = 1
color_collar_socks       = 2
color_skin_hair          = 3
color_eyes_shoes_handles = 4
color_rope               = 5

steps = [
  [ # Step 0
    [ layer_main,               layer_main,
      color_main,               color_main ],

    [ layer_collar_socks,       layer_collar_socks,
      color_collar_socks,       color_collar_socks ],

    [ layer_skin_hair,          layer_skin_hair,
      color_skin_hair,          color_skin_hair ],

    [ layer_eyes_shoes_handles, layer_eyes_shoes_handles,
      color_eyes_shoes_handles, color_eyes_shoes_handles ],

    [ layer_rope_front,         layer_rope_front,
      color_rope,               color_rope ],

    [ layer_rope_top,           layer_rope_top,
      color_background,         color_background ]
  ],
  [ # Step 1
    [ layer_rope_bottom,        layer_rope_bottom,
      color_rope,               color_rope ],

    [ layer_rope_front,         layer_rope_front,
      color_background,         color_background ]
  ],
  [ # Step 2
    # Do nothing
  ],
  [ # Step 3
    [ layer_rope_back,          layer_rope_back,
      color_rope,               color_rope ],

    [ layer_rope_bottom,        layer_rope_bottom,
      color_background,         color_background ]
  ],
  [ # Step 4
    [ layer_rope_top,           layer_rope_top,
      color_rope,               color_rope ],

    [ layer_rope_back,          layer_rope_back,
      color_background,         color_background ]
  ],
  [ # Step 5
    # Do nothing
  ],
]

step_speed = 200
