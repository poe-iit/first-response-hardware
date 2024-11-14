import time
from machine import Pin, PWM
from utils.load_env import load_env

env = load_env()

class Alarm:
  def __init__(self, frequency, duration, tone_volume):
    audio_pin = int(env.get("AUDIO_PIN"))
    self.audio = PWM(Pin(audio_pin))
    self.audio.duty_u16(0)
    self.frequency = frequency
    self.duration = duration
    self.tone_volume = tone_volume
  
  def play_tone(self):
    if self.frequency == 0:
      self.audio.duty_u16(0)
      time.sleep(self.duration) #bug
    self.audio.freq(self.frequency)
    self.audio.duty_u16(int(self.tone_volume * 65535))  # 50% duty cycle
    time.sleep(self.duration)
    self.audio.duty_u16(0)
  
  def play_alarm(self, iterations):
    for _ in range(iterations):
      self.play_tone()
      time.sleep(0.1)

