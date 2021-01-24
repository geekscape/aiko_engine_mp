import time
from lib.aiko import led

# from examples.badge_np import run; run()

# this is set by aiko/led.py and configured in configuration/led.py
#num_np = 46
#np = neopixel.NeoPixel(machine.Pin(19), 46)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)
 
 
def rainbow_cycle(num_np, wait):
    for j in range(255):
        for i in range(num_np):
            pixel_index = (i * 256 // num_np) + j
            led.pixel(wheel(pixel_index & 255), i)
        led.write()
        time.sleep(wait)
 
 
def run():
    led.initialise()

    time.sleep(25)

    while True:
        led.fill((255, 0, 0))
        led.write()
        time.sleep(1)
     
        led.fill((0, 255, 0))
        led.write()
        time.sleep(1)
     
        led.fill((0, 0, 255))
        led.write()
        time.sleep(1)
     
        rainbow_cycle(led.length_get(), 0.001)  # rainbow cycle with 1ms delay per step

