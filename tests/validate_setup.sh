#!/bin/bash

# Test audio input
arecord -d 3 -c 1 -r 16000 -f S16_LE test.wav
aplay test.wav

# Test GPIO
if [ "$USE_HARDWARE_BUTTON" = "True" ]; then
    python3 - <<END
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
print("GPIO17 input:", GPIO.input(17))
GPIO.cleanup()
END
fi

# Test model loading
python3 - <<END
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/Janus-Pro-1B")
print("Tokenizer loaded successfully!")
END 