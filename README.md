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

### 1. Clone Repository (Using SSH)
```bash
git clone git@github.com:yourusername/pi-ai-assistant.git
cd chat_assistant_pi
```

### 2. Prepare Setup Script
```bash
# Install line ending converter
sudo apt-get install dos2unix -y

# Fix file formatting
dos2unix setup.sh
chmod +x setup.sh
```

### 3. Run Installation
```bash
# Install dependencies (run with sudo)
./setup.sh

# If Python environment fails, create manually
python3 -m venv ai-env
source ai-env/bin/activate
```

### 4. Post-Installation Checks
```bash
# Run validation tests
python tests/validate_setup.py

# Start service manually
sudo systemctl daemon-reload
sudo systemctl start ai-assistant
```

### Important Notes
- Replace `yourusername` in clone URL with your actual GitHub username
- For GitHub authentication issues:
  1. [Create personal access token](https://github.com/settings/tokens)
  2. Use token as password in HTTPS clone:
  ```bash
  git clone https://yourusername:your_token@github.com/yourusername/pi-ai-assistant.git
  ```
- If seeing `--break-system-packages` errors, append to pip commands:
  ```bash
  pip install package_name --break-system-packages
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

### 3. Virtual Environment Management
```bash
# Activate environment (required for manual operation):
source ai-env/bin/activate

# Deactivate environment:
deactivate

# For systemd service, activation is automatic
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
source ai-env/bin/activate  # If not already activated
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

4. Fix audio device priority:
   ```bash
   sudo nano /etc/modprobe.d/alsa-base.conf
   # Add: options snd-usb-audio index=0
   sudo reboot
   ```

## License
MIT License - See [LICENSE](LICENSE) for details
