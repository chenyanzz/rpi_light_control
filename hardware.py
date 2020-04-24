import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BCM)

def tini():
    GPIO.cleanup()

class Switch(object):
    gpio_port = 11
    is_on = False
    bouncetime = 200
    on_state_change = lambda is_on: 'do something'

    def init(self, on_state_change):
        self.on_state_change = on_state_change

        GPIO.setup(self.gpio_port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.gpio_port, GPIO.BOTH,bouncetime=self.bouncetime, callback= lambda channel: self.on_gpio_interrupt())

    def on_gpio_interrupt(self):
        # button pull-up, so level LOW is clicked
        if GPIO.input(self.gpio_port):
            self.on_state_change(False)
        else:
            self.on_state_change(True)


class Light(object):
    gpio_port = 8
    is_on = False

    def init(self):
        GPIO.setup(self.gpio_port, GPIO.OUT)
        self.turnOn()

        
    def turnOn(self):
        self.is_on = True
        GPIO.output(self.gpio_port, True)

    def turnOff(self):
        self.is_on = False
        GPIO.output(self.gpio_port, False)

    def flipState(self):
        if self.is_on:
            self.turnOff()
        else:
            self.turnOn()
