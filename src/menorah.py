from picozero import LED, Button
from math import radians, cos, exp
from time import sleep
import asyncio

pins = 15,14,13,12,16,17,18,19  # software untangling of scrambled wires in prototype
leds = [LED(pin) for pin in pins]

blue_button = Button(26, pull_up = False)
green_button = Button(27, pull_up = False)
red_button = Button(28, pull_up = False)


class Menorah(object):
    def __init__(self):
        self.lock = asyncio.Lock()
        self.lights = 1
        for led in range(8):
            self.led_on_off(led, 1/8)
        self.display_lights()

    def led_on_off(self, led, delay=1):
        leds[led].on()
        sleep(delay)
        leds[led].off()

    def display_lights(self):
        for led in leds[:self.lights]:
            led.on()
        for led in leds[self.lights:]:
            led.off()

    async def party_time(self):
        # this method is an extremely messy work in progress
        async with self.lock:
            """for i in range(15):
                sleep(.1)
                for x in range(8):
                    leds[x].on()
                    leds[x-1].off()
                    sleep(.01)
                leds[7].off()
                '''sleep(.01)
                for x in range(7,0,-1):
                    leds[x-1].on()
                    leds[x].off()
                    sleep(.01)
                leds[0].off()  '''"""

            #for i in range(360*2):
            #    for n, led in enumerate(leds):
            #        led.brightness = 0.51 + 0.49 * cos(radians(i-n*20))
            #    sleep(0.01

            for t in range(1024+1):
                #print('')
                for n, led in enumerate(leds):
                    #n = -4.5
                    x = t/1024-(2*n+9)/32
                    led.brightness = exp(-200*x*x)
                    #sleep(0.001)
                    #print(t, x, exp(-200*x*x))
                #print(led.brightness)
                await asyncio.sleep(0)
            self.display_lights()

    async def add_light(self):
        if self.lights < len(leds):
            async with self.lock:
                peak_position = len(leds) + 1  # Start with the Gaussian peak just off the end
                target_position = self.lights  # Position of the new LED to be added

                while peak_position >= target_position:
                    for i, led in enumerate(leds):
                        if i < self.lights:  # Already lit LEDs remain at full brightness
                            led.brightness = 1.0
                        else:  # Update brightness for other LEDs based on the Gaussian curve
                            x = (i - peak_position) / len(leds)
                            led.brightness = exp(-200 * x * x)

                    peak_position -= .05  # Move the Gaussian peak leftward
                    await asyncio.sleep(0)

                self.lights += 1
                self.display_lights()

    async def del_light(self):
        if self.lights > 0:
            async with self.lock:
                peak_position = self.lights - 1  # Start with the Gaussian peak at the last lit LED
                target_position = len(leds) +1 # Peak moves to the rightmost position

                while peak_position <= target_position:
                    for i, led in enumerate(leds):
                        if i < self.lights - 1:  # LEDs below the current stack remain fully lit
                            led.brightness = 1.0
                        else:  # Update brightness for the peak position dynamically
                            x = (i - peak_position) / len(leds)
                            led.brightness = exp(-200 * x * x)

                    peak_position += 0.05  # Move the Gaussian peak rightward
                    await asyncio.sleep(0)

                self.lights -= 1


menorah = Menorah()
green_button.when_pressed = lambda: asyncio.run(menorah.add_light())
red_button.when_pressed = lambda: asyncio.run(menorah.del_light())
blue_button.when_pressed = lambda: asyncio.run(menorah.party_time())
