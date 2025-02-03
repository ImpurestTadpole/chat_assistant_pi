# Install system dependencies
sudo apt-get update && sudo apt-get install -y \
    portaudio19-dev \
    libportaudio2 \
    libatlas-base-dev \
    ffmpeg \
    libasound2-dev \
    libjack-dev \
    sox \
    python3-rpi.gpio \
    python3-tk \
    python3-venv

# Create virtual environment
python3 -m venv ai-env
source ai-env/bin/activate

# Install Python packages
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install pyaudio
pip install transformers datasets sounddevice scipy sentencepiece deepseek-api
pip install bitsandbytes
pip install RPi.GPIO
pip install pillow
pip install einops
pip install accelerate

# Add hardware permissions
sudo usermod -a -G gpio $USER
sudo usermod -a -G audio $USER

# Create udev rule for hardware button (if used)
echo 'SUBSYSTEM=="input", GROUP="input", MODE="0666"' | sudo tee /etc/udev/rules.d/99-com.rules

# For GUI mode (default)
python app.py

# For hardware button mode
sed -i 's/USE_HARDWARE_BUTTON = False/USE_HARDWARE_BUTTON = True/' app.py
python app.py

sudo systemctl daemon-reload
sudo systemctl enable ai-assistant.service

