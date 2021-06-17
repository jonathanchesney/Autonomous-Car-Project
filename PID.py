# Jonathan Chesney Paul Takhar Joshua Rossie
# Import libaries needed
from pyb import LED
import time, utime
from pyb import Pin, Timer
import sensor, image, time, math, pyb

usb = pyb.USB_VCP() # This is a serial port object that allows you to
# Communciate with your computer. While it is not open the code below runs.

# DIR pins on motor driver should be set low, so the car goes forward, set to -1 to go backwards
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_DOWN)
pin1 = Pin('P1', Pin.OUT_PP, Pin.PULL_DOWN)
pin2 = Pin('P2', Pin.OUT_PP, Pin.PULL_DOWN)


# Initilaze leds
red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)
ir_led    = LED(4)

# Initialize timers and set their pin number as well as frequency
tim4 = Timer(4, freq=500) # Frequency in Hz, Motor
tim2 = Timer(2, freq=150)

# Color values, you will have to adjust these values depending on lighting so that it can accuratly identify blob
# General range for a white line is like 160-255
GRAYSCALE_THRESHOLD = [(200, 255)]

# Here we set up the region of interest, this program only has one region of interest
ROI= (0, 60, 160, 20)

# Camera setup...
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # use grayscale.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock() # Tracks FPS.

# This is the initial pulse width percent the motor starts at
init = 80;

# Variable used down below
PWMvalue = 0;

# We want the blobs x position to be at x = 80, 80 is the middle of the picture
# The line needs to be in the center of the screen
setpoint=80;

# Variable used down below
previousError=0;

# We change these two variables based on how the car is performing,
# look up how to tune PID online for more info
Kp = .60;
Kd = .25;

# Keep leds on to helpo illuminate the track
blue_led.on()
green_led.on()
red_led.on()

error1 = 0;

run = 0;

Out1 = Pin('P0',Pin.OUT_PP)
In1 = Pin('P1',Pin.IN)
DIR = Pin('P2',Pin.OUT_PP)

start = 0;
end = 0;

delta = 0;

while(run <1):

    Out1.low()         #-
    utime.sleep_us(5)  # -
    Out1.high()        #  - These lines create a pulse of width 10us
    utime.sleep_us(10) # -  to be sent to the trig input of the sensor
    Out1.low()         #-


    while(0==In1.value()):      # This loop waits until the output from the sensor
                                # equals 1 and then records the time
        start = utime.ticks_us()

    while(1==In1.value()):      # This loop waits until the output from the sensor
                                # stops equaling one and then records the time
        end = utime.ticks_us()


    delta = end -start          # This line finds the difference in time from the start
                                # of the senor output pulse (rising edge) to the end (falling edge)

    dist = (delta/10000)/2 *343 # Converts the tiume to a distance in cm

    print(dist)
    if(dist <20):
        motorR = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent = 0)
        motorL = tim4.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent = 0)
        utime.sleep_ms(1000)
        DIR.high()
        motorL = tim4.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent = 30)
        motorR = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent = 30)
        utime.sleep_ms(830)
        motorR = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent = 0)
        DIR.low()

    clock.tick()                # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()     # Take a picture and return the image.


    # This identifies blobs within the region of interest that fit our pixel and area threshold
    blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi=ROI[0:4], pixels_threshold=10, area_threshold=10,merge=False)

    # count keeps track of how many blobs are on the screen
    count = 0;

    # Adds up the number of blobs in our region of interest, this is important so that we can idetify the finish line (3 blobs) and main track (1 blob) and no track (0 blobs)
    for i in blobs:
        count += 1

    # If there is one blob then we are on the course and the code below is run
    if(count == 1):
        largest_blob = max(blobs, key=lambda b: b.pixels()) #


        # Draw a rect around the blob. This is just so we can see the blob rectangle on the camera
        img.draw_rectangle(largest_blob.rect())
        img.draw_cross(largest_blob.cx(),
        largest_blob.cy())
        xpos=largest_blob.cx()
        print("xpos is /n")
        print(xpos)

        # At this point the blob has been indentified and is displayed on the screen

    # PID

        # This gets the x position of the blob and subtracts it from our desired x position which is
        # 80, this generates the error1 term which tells us how far away the blob is from the center
        # of the screen
        error1= largest_blob.cx()-setpoint;

    # Not needed but shows the error value
    # print("error is ")
    # print(error1)

    #PD calculation
    p = error1;

    d = error1-previousError;

    PIDvalue= (Kp*p) + (Kd*d);

    previousError = error1;

    # If error1 > 0 then the car is left of the track
    if error1 > 0:
        motorR = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent = init + PIDvalue)
        motorL = tim4.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent = init - PIDvalue)
    # If error1 < 0 then the car is right of the track
    if error1 < 0:
        motorR = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent = init + PIDvalue)
        motorL = tim4.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent = init - PIDvalue)




    # Else if the number of blobs is zero then we are not on the track and the code below exceutes
    elif(count == 0):
        motorR = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent = 0)
        motorL = tim4.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent = 0)

        print("off track")

        print("all leds off")
        # We maintain the last pw by not changing anything therefore it stays the same as last time the blob loop ran
        blue_led.on()
        green_led.on()
        red_led.on()


    # Else if the number of blobs is 3 then we have reached the finish line
    elif(count == 3):

        motorR = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent = 0)
        motorL = tim4.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent = 0)

        print("finish line detected")

        print("all leds on")
        blue_led.on()
        green_led.on()
        red_led.on()
        run = run +1;


#the end
