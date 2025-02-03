import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, MultiModalityCausalLM
import threading
import tkinter as tk
from tkinter import ttk
import torch
import psutil
import time

# Configuration
FS = 16000  # Sample rate
RECORD_SECONDS = 5
USE_HARDWARE_BUTTON = False  # Set to True for physical button

if USE_HARDWARE_BUTTON:
    import RPi.GPIO as GPIO
    from time import sleep
    BUTTON_PIN = 17
    LED_PIN = 18

class AssistantUI(tk.Tk):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.title("AI Assistant")
        self.geometry("300x200")
        
        self.create_widgets()
        self.check_hardware_button()
        
    def create_widgets(self):
        self.btn_talk = ttk.Button(
            self, 
            text="Hold to Speak", 
            command=self.start_recording
        )
        self.btn_talk.pack(pady=20)
        
        self.status_label = ttk.Label(self, text="Ready")
        self.status_label.pack(pady=10)
        
        self.response_text = tk.Text(self, height=5, width=30)
        self.response_text.pack(pady=10)
        
    def start_recording(self):
        self.status_label.config(text="Recording...")
        self.update_idletasks()
        
        # Run recording in separate thread
        threading.Thread(target=self.process_request).start()
        
    def process_request(self):
        audio = self.assistant.record_audio()
        self.status_label.config(text="Processing...")
        
        text = self.assistant.stt(audio)["text"]
        response = self.assistant.process_query(text)
        
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)
        self.status_label.config(text="Ready")
        
        self.assistant.play_response(response)
        
    def check_hardware_button(self):
        if USE_HARDWARE_BUTTON:
            threading.Thread(target=self.hardware_button_listener).start()
            
    def hardware_button_listener(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LED_PIN, GPIO.OUT)
        
        while True:
            GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
            self.start_recording()

class PiAssistant:
    def __init__(self):
        if USE_HARDWARE_BUTTON:
            self.setup_hardware()
            
        # Speech-to-Text
        self.stt = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny",
            device="cpu"
        )
        
        # Text Generation with Janus-Pro
        self.tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/Janus-Pro-1B")
        self.model = MultiModalityCausalLM.from_pretrained(
            "deepseek-ai/Janus-Pro-1B",
            load_in_8bit=True,
            device_map="auto",
            trust_remote_code=True
        )
        
        # Text-to-Speech
        self.tts = pipeline(
            "text-to-speech",
            model="facebook/mms-tts-eng",
            device_map="auto"
        )

        # Add to PiAssistant __init__
        torch.set_flush_denormal(True)
        torch.backends.optimized = True

    def setup_hardware(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LED_PIN, GPIO.OUT)

    def record_audio(self):
        print("Recording...")
        recording = sd.rec(int(RECORD_SECONDS * FS), 
                         samplerate=FS, 
                         channels=1,
                         dtype='float32')
        sd.wait()
        return recording.reshape(-1)

    def process_query(self, text):
        inputs = self.tokenizer(
            text, 
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def run(self):
        print("Ready - Press button to speak")
        while True:
            temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
            if temp > 75:  # Celsius
                print(f"High temperature warning: {temp}°C")
                self.play_response("System temperature critical, cooling down")
                time.sleep(30)
            
            # Wait for button press
            GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
            GPIO.output(LED_PIN, True)
            
            # Record while button is held
            audio = self.record_audio()
            GPIO.output(LED_PIN, False)
            
            # Process and respond
            text = self.stt(audio)["text"]
            print(f"You said: {text}")
            
            response = self.process_query(text)
            print(f"Assistant: {response}")
            
            # Blink LED during response
            self.play_response(response)

    def play_response(self, response):
        speech = self.tts(response)
        for _ in range(3):
            GPIO.output(LED_PIN, True)
            sd.play(speech["audio"][0], speech["sampling_rate"])
            sd.wait()
            GPIO.output(LED_PIN, False)
            sleep(0.2)

if __name__ == "__main__":
    assistant = PiAssistant()
    
    if USE_HARDWARE_BUTTON:
        try:
            assistant.run()
        finally:
            if USE_HARDWARE_BUTTON:
                GPIO.cleanup()
    else:
        ui = AssistantUI(assistant)
        ui.mainloop()