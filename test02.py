from Utils.HIDMedia.media import Media
from Utils.HIDMedia.media_keys import *

# Media.send_key(KEY_MEDIA_VOLUME_UP)
# Media.send_key(KEY_MEDIA_VOLUME_DOWN)
# Media.send_key(KEY_MEDIA_MUTE)
#
# Media.send_key(KEY_MEDIA_PLAY)
# Media.send_key(KEY_MEDIA_PAUSE)
#
# Media.send_key(KEY_MEDIA_NEXT_TRACK)
# Media.send_key(KEY_MEDIA_PREV_TRACK)
# Media.send_key(KEY_MEDIA_STOP)

import time
# from media import Media
# from media_keys import *

MEDIA_KEYS = [
    ("VOLUME UP", KEY_MEDIA_VOLUME_UP),
    ("VOLUME DOWN", KEY_MEDIA_VOLUME_DOWN),
    ("MUTE", KEY_MEDIA_MUTE),
    ("PLAY", KEY_MEDIA_PLAY),
    # ("PAUSE", KEY_MEDIA_PAUSE),
    ("NEXT TRACK", KEY_MEDIA_NEXT_TRACK),
    ("PREVIOUS TRACK", KEY_MEDIA_PREV_TRACK),
    ("STOP", KEY_MEDIA_STOP),
]

DELAY_SECONDS = 3
REPEAT_COUNT = 2

for name, key in MEDIA_KEYS:
    for i in range(REPEAT_COUNT):
        print(f"Sending {name} ({i + 1}/{REPEAT_COUNT})")
        Media.send_key(key)
        time.sleep(DELAY_SECONDS)

