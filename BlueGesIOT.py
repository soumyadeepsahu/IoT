from machine import Pin, UART
import time

#Bluetooth
uart = UART(0,9600)


# Set up the input pins for the sensors
sensor1_pin = Pin(16, Pin.IN)
sensor2_pin = Pin(18, Pin.IN)
blue_pin = Pin(15, Pin.OUT)
green_pin = Pin(14, Pin.OUT)
red_pin = Pin(13, Pin.OUT)

#counters
countRight = 0
current_color = -1

#define the next LED function that changes the color of the LED
def toggle_color(color_num):
    # Turn on all LEDs
    red_pin.on()
    green_pin.on()
    blue_pin.on()

    # Update the current color
    global current_color
    current_color += color_num
    
    print(current_color)
    # Turn off the LED corresponding to the current color
    if current_color == 0:
        red_pin.off()
    elif current_color == 1:
        green_pin.off()
    elif current_color == 2:
        blue_pin.off()
    else:
        red_pin.on()
        green_pin.on()
        blue_pin.on()
        current_color = -1
    
    
#by default the LEDs will be off
red_pin.on()
green_pin.on()
blue_pin.on()
        
# Main loop to constantly read sensor values
while True:
    sensor1_val = sensor1_pin.value()
    sensor2_val = sensor2_pin.value()
    
    if(sensor1_val == 0):
        countRight += 1
    while countRight == 1:
        sensor1_val = sensor1_pin.value()
        sensor2_val = sensor2_pin.value()
        if(sensor2_val == 0):
            countRight += 1
            print("Sensor 2: ", sensor2_val)
            time.sleep(1)
        if(countRight >= 2):
            toggle_color(1)
            #red_pin.off()
            countRight = 0
            #print("Sensor 2: ", sensor2_val)
        time.sleep(0.1)
    
    time.sleep(0.1) # delay of 0.1 seconds
    
    if uart.any():
        input_str = uart.readline().decode()
        print(input_str)
        if input_str == "off\r\n":
            red_pin.on()
            green_pin.on()
            blue_pin.on()
        elif input_str == "r\r\n":
            red_pin.value(0)
            green_pin.on()
            blue_pin.on()
        elif input_str == "b\r\n":
            blue_pin.value(0)
            red_pin.on()
            green_pin.on()
        elif input_str == "g\r\n":
            green_pin.value(0)
            red_pin.on()
            blue_pin.on()
    time.sleep(0.1)


