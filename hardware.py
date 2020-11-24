import RPi.GPIO as GPIO
import threading
import time

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def tini():
    GPIO.cleanup()

class Switch(object):
    gpio_port = 7
    is_on = False
    bouncetime = 400
    on_state_change = lambda is_on: 'do something'
    timer = None
    mutex = threading.Lock()

    def init(self, on_state_change):
        self.on_state_change = on_state_change
        GPIO.setup(self.gpio_port, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.on_timer_event()
        
        # GPIO.add_event_detect(self.gpio_port, GPIO.BOTH,bouncetime=self.bouncetime, callback= lambda channel: self.on_gpio_interrupt())
        
        print("The switch is on PORT%s"%self.gpio_port)

    def on_timer_event(self):
        self.mutex.acquire()
        try:
            stat = not GPIO.input(self.gpio_port)
            if stat != self.is_on:
                time.sleep(0.05)
                if stat != self.is_on:
                    self.is_on = stat
                    self.on_state_change(stat)
        finally:
            self.mutex.release()
            self.timer = threading.Timer(0.25, self.on_timer_event)
            self.timer.setDaemon(True)
            self.timer.start()

    # def on_gpio_interrupt(self):
    #     # button pull-up, so level LOW is clicked
    #     if GPIO.input(self.gpio_port):
    #         print("The button reads HIGH")
    #         self.on_state_change(False)
    #     else:
    #         print("The button reads LOW")
    #         self.on_state_change(True)


class Light(object):
    gpio_port = 8
    is_on = False
    mutex = threading.Lock()

    def init(self):
        GPIO.setup(self.gpio_port, GPIO.OUT)
        self.turnOn()
        print("The light is on PORT%s"%self.gpio_port)

        
    def turnOn(self):
        print("The light now turns on")
        self.is_on = True
        GPIO.output(self.gpio_port, True)

    def turnOff(self):
        print("The light now turns off")
        self.is_on = False
        GPIO.output(self.gpio_port, False)
        

    def flipState(self):
        self.mutex.acquire()
        if self.is_on:
            self.turnOff()
        else:
            self.turnOn()
        self.mutex.release()
