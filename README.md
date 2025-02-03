# Raspberry Pi AI Assistant

A voice-enabled AI assistant with hardware/software interface options, powered by DeepSeek's Janus-Pro-1B model.

## Features
- 🎙️ Voice input via microphone
- 🤖 Multi-modal AI responses
- 🎧 Text-to-speech output
- 🖥️ GUI and hardware button interfaces
- 🔌 Auto-start service configuration

## Hardware Requirements
- Raspberry Pi 4 (4GB+ RAM recommended)
- USB Microphone or GPIO-compatible audio input
- Speaker/3.5mm audio output
- (Optional) Momentary button & LED for hardware control

## Installation

### 1. System Setup
```bash
# Clone repository
git clone https://github.com/yourusername/pi-ai-assistant.git
cd pi-ai-assistant

# Run automated setup (takes 15-30 minutes)
bash <(curl -sL https://raw.githubusercontent.com/yourusername/pi-ai-assistant/main/setup.sh)

# OR if you have the setup.sh locally:
./setup.sh
```

### 2. Hardware Setup (Optional)
```