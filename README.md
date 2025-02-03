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

# Install dependencies and setup environment
chmod +x setup.sh
./setup.sh

# Reboot after installation
sudo reboot
```

### 2. Hardware Setup (Optional)
```text
Button Connection:
- Button leg 1 → GPIO17
- Button leg 2 → GND

LED Connection:
- LED anode (long leg) → 330Ω resistor → GPIO18
- LED cathode (short leg) → GND
```

## Configuration

### Modes of Operation
| Mode          | Configuration                 | Description                  |
|---------------|-------------------------------|------------------------------|
| GUI Mode      | `USE_HARDWARE_BUTTON = False` | Default touchscreen interface|
| Hardware Mode | `USE_HARDWARE_BUTTON = True`  | Physical button controlled   |

Switch modes by editing `app.py`:
```bash
nano app.py  # Change USE_HARDWARE_BUTTON value
```

### Auto-Start Service
```bash
sudo systemctl enable ai-assistant
sudo systemctl start ai-assistant
```

## Usage

### Hardware Mode
1. Press and hold button to record
2. Release to process query
3. LED indicates processing status

### GUI Mode
```bash
source ai-env/bin/activate
python app.py
```
- Click "Hold to Speak" button
- View responses in text window
- Status indicators show processing state

## Technical Specifications

| Component       | Requirement                          |
|-----------------|--------------------------------------|
| OS              | Raspberry Pi OS (64-bit)             |
| Python          | 3.7+                                 |
| RAM Usage       | 2.5GB (idle) - 3.8GB (processing)    |
| Storage         | 8GB+ free space                      |

## Troubleshooting

### Common Issues
1. **Audio Not Working**
   ```bash
   # Test microphone
   arecord -d 5 test.wav
   aplay test.wav
   ```
   
2. **Model Loading Errors**
   ```bash
   # Free up memory
   sudo swapoff -a
   sudo swapon -a
   ```

3. **GPIO Permissions**
   ```bash
   sudo usermod -a -G gpio $USER
   sudo reboot
   ```

## Final Setup Steps
1. Enable SPI and I2C interfaces:
   ```bash
   sudo raspi-config
   # -> Interface Options -> Enable SPI/I2C
   ```

2. Increase swap space for model loading:
   ```bash
   sudo nano /etc/dphys-swapfile
   # Change CONF_SWAPSIZE=2048
   sudo systemctl restart dphys-swapfile
   ```

3. Verify audio routing:
   ```bash
   alsamixer  # Press F6 to select correct sound card
   ```

## License
MIT License - See [LICENSE](LICENSE) for details
