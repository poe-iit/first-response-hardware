from machine import Pin, PWM, Timer
from time import sleep
import neopixel
import math
import functions as driver


print("testing directional arrows")

driver.generateNorth()
sleep(0.25)
driver.generateSouth()
sleep(0.25)
driver.generateEast()
sleep(0.25)
driver.generateWest()
sleep(0.25)

print("testing cross")
driver.clearAllNP()
driver.crossBlinking()
print("terminating code")
driver.clearAllNP()
