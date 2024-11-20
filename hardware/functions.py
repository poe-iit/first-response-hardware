from machine import Pin, ADC, PWM, Timer
from time import sleep
import neopixel
import math

NORTH = [0,1,0,1]
SOUTH = [1,0,1,0]
EAST = [1,0,0,1]
WEST = [0,1,1,0]
DIRS = [NORTH, SOUTH, EAST, WEST]

# Hardware-Based Constants

# Pin Numbers on hardware
audioPinNumber = 33
dirLEDPinNumber = 14
crossLEDPinNumber = 27

audio_pin = PWM(Pin(audioPinNumber))
dirPin = Pin(dirLEDPinNumber)
crossPin = Pin(crossLEDPinNumber)


# LED Constants
dirColor = (0, 255, 0)
crossColor = (255, 0, 0)
dirLen = 24
crossLen = 24
 
dirNeo = neopixel.NeoPixel(dirPin, dirLen)
crossNeo = neopixel.NeoPixel(crossPin, crossLen)
# Audio Constants
freq = 2200
dur = 0.12
tone_volume = 0.65  # 65% volume

def dirNP():
    return (dirNeo, dirLen, dirColor)
def crossNP():
    return (crossNeo, crossLen, crossColor)

def audioSetup():
    return (Pin(audioPinNumber), freq, dur)

# LED functions
def arrayToLine(np, length, color, array):
    for chunk in range(len(array)):
        if(array[chunk] == 1):
            quarterLine(np, length, color, chunk)
    sleep(0.25)
    np.write()
    
def quarterLine(np, length, color, direction = 0):
    for i in range(math.floor(length/4)):
        np[i + (direction * math.floor(length/4))] = color

def clearNP(np):
    np.fill((0,0,0))
    np.write()

def clearAllNP():
    clearNP(dirNeo)
    clearNP(crossNeo)

def generateCross(np, color):
    print("Generating Cross")
    clearNP(np)
    np.fill(color)
    np.write()
    
def generateCrossDriver(color):
    generateCross(crossNeo, color)
    
def crossBlinking():
    for i in range(4):
        generateCross(crossNeo, crossColor)
        playAlarm(2200, 0.12, 4)
        sleep(0.25)
        clearNP(crossNeo)
        sleep(1)

# Givena direction array, light up leds
def generateDirection(np, length, color, dir):
    clearNP(np)
    sleep(0.1)
    arrayToLine(np, length, color, dir)
    np.write()

def testDirections():
    for dir in DIRS:
        generateDirection(dirNeo, dirLen, dirColor, dir)
        sleep(0.75)

def generateNorth():
    clearNP(dirNeo)
    print("Generating Direction LED: NORTH")
    generateDirection(dirNeo, dirLen, dirColor, NORTH)
    
def generateSouth():
    clearNP(dirNeo)
    print("Generating Direction LED: SOUTH")
    generateDirection(dirNeo, dirLen, dirColor, SOUTH)
    
def generateEast():
    clearNP(dirNeo)
    print("Generating Direction LED: EAST")
    generateDirection(dirNeo, dirLen, dirColor, EAST)
    
def generateWest():
    clearNP(dirNeo)
    print("Generating Direction LED: WEST")
    generateDirection(dirNeo, dirLen, dirColor, WEST)
    
# Speaker Functions

audio_pin.duty_u16(0)  # Start with no sound

def play_tone(frequency, duration):
    if frequency == 0:  # Silence
        audio_pin.duty_u16(0)
        time.sleep(duration)
        return

    # Set the PWM frequency
    audio_pin.freq(frequency)
    # Set duty cycle to a scaled value for volume
    audio_pin.duty_u16(int(tone_volume * 65535))  # 50% duty cycle
    sleep(duration)  # Play for the specified duration
    # Turn off the sound after the tone
    audio_pin.duty_u16(0)

def playAlarm(freq, dur, iter):
    for i in range(iter):
        play_tone(freq, dur)
        sleep(0.1)

def loopAlarm(freq, dur, iter):
    for i in range(iter):
        playAlarm(freq, dur, 4)
        sleep(0.8)

