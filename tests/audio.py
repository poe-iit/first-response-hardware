
import time
from utils.audio import Alarm
from utils.load_env import load_env

env = load_env()
audio_volume = float(env.get("AUDIO_VOLUME"))

time.sleep(5)

detected_fire = True

def alarm_task(*args, **kwargs):
  alarm = Alarm(*args, **kwargs)
  alarm.stop_tone()
  playing_alarm = False
  play_alarm_gen = None
  # alarm.play_alarm(4)

  next_execution = time.ticks_ms() / 1_000
  while True:
    current_time = time.ticks_ms() / 1_000
    if playing_alarm and play_alarm_gen:
      try:
        next(play_alarm_gen)
      except StopIteration:
        print("Alarm stopped, waiting 0.8 seconds")
        playing_alarm = False
        play_alarm_gen = None
        next_execution = (time.ticks_ms() / 1_000) + 0.8
    elif current_time >= next_execution and detected_fire:
      playing_alarm = True
      play_alarm_gen = alarm.play_alarm(4)
    yield


# To make the alarm and crossing tasks run in parallel
def alert_floor(color, *args, **kwargs):
  alarm_gen = alarm_task(*args, **kwargs)

  while True:
    next(alarm_gen)
    # time.sleep(0.1)

# Replace 0.2 with 0.12 later
alert_floor((255, 0, 0), 2200, 0.12, audio_volume)
print("Done")