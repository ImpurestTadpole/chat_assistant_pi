# Update these paths at the top
USER_HOME="/home/$(logname)"
PROJECT_DIR="${USER_HOME}/chat_assistant_pi"
VENV_DIR="${PROJECT_DIR}/ai-env"

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
    python3-venv \
    libopenblas-dev \
    python3-full

# Create virtual environment with specific Python version
python3.10 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

# Install Python packages
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --break-system-packages
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
echo 'SUBSYSTEM=="input", GROUP="input", MODE="0666"' | sudo tee "/etc/udev/rules.d/99-com.rules"

# For GUI mode (default)
python "${PROJECT_DIR}/app.py"

# For hardware button mode
sed -i 's/USE_HARDWARE_BUTTON = False/USE_HARDWARE_BUTTON = True/' "${PROJECT_DIR}/app.py"
python "${PROJECT_DIR}/app.py"

sudo systemctl daemon-reload
sudo systemctl enable ai-assistant.service

# Optimize memory limits
echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf
echo "vm.min_free_kbytes = 65536" | sudo tee -a /etc/sysctl.conf

# Install remaining dependencies manually
pip install \
    transformers==4.48.2 \
    datasets==3.2.0 \
    scipy==1.15.1 \
    sentencepiece==0.2.0 \
    --break-system-packages

# Add explicit sounddevice install
pip install \
    sounddevice \
    transformers datasets \
    --break-system-packages

# Update systemd service configuration
sudo tee "/etc/systemd/system/ai-assistant.service" <<EOF
[Unit]
Description=AI Assistant Service
After=network.target

[Service]
Environment="LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libatomic.so.1"
ExecStart=${VENV_DIR}/bin/python ${PROJECT_DIR}/app.py
WorkingDirectory=${PROJECT_DIR}
User=$(whoami)
Restart=always

[Install]
WantedBy=multi-user.target
EOF

