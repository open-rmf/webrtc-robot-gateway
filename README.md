# webrtc-robot-gateway

## Installation Instructions

### Setup
```
# Install Raspberry Pi OS on Rpi4
https://www.raspberrypi.org/software/operating-systems/

apt update && apt upgrade
apt install avahi-daemon openssh-server
# In /boot/config.txt, set force_hdmi_hotplug=1, enable_uart=1
raspi-config # Enable webcam
echo "bcm2835-v4l2" | sudo tee -a /etc/modules
```

### Set up and test connectivity with Robot Base ( Sphero RVR )
```
cd; git clone https://github.com/sphero-inc/sphero-sdk-raspberrypi-python.git
cd sphero-sdk-raspberrypi-python; sh first-time-setup.sh
pip3 install aiohttp pyserial_asyncio
usermod -aG tty $USER
usermod -aG dialout $USER 
cd projects/keyboard_control
python3 drive_with_wasd_keys.py

echo "export PYTHONPATH=$PYTHONPATH:$HOME/sphero-sdk-raspberrypi-python" >> ~/.bashrc
```

### Set up DroidCam if using Android Phone for Camera ( Caution, Rpi might not be able to handle the high data bandiwidth )
```
# On phone, install DroidCam Android App from App Store

# On Rpi4: https://github.com/dev47apps/droidcam/wiki/Raspberry-PI
apt install adb cmake unzip

##  libjpeg-turbo from source
wget https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/2.1.0.zip
unzip 2.1.0.zip; cd libjpeg-turbo-2.1.0
cmake -G "Unix Makefiles" .
make; sudo make install

## droidcam from source
cd; git clone https://github.com/dev47apps/droidcam.git; cd droidcam
apt install raspberrypi-kernel-headers
apt install libavutil-dev libswscale-dev libasound2-dev libspeex-dev libusbmuxd-dev libplist-dev
make droidcam-cli
./install-client
./install-video
./install-sound
cp droidcam-cli /usr/bin
reboot

# Test droidcam
## On mobile, run droidcam app
## On rpi4
apt install streamer pavucontrol
adb devices
sudo droidcam-cli adb 4747 # Replace 4747 with whatever port is specified on app screen
streamer -f jpeg -o image.jpeg

```

### Install aiortc
```
apt install libavdevice-dev libavfilter-dev libopus-dev libvpx-dev pkg-config python3-pip
pip3 install aiortc aiohttp
cd; git clone https://github.com/aiortc/aiortc.git
```
```

### Set up Wireguard
```
apt install wireguard
# Set up config files
```
### Run
```
wg-quick up wg0
sudo droidcam-cli adb 4747   # If using mobile phone as camera
python3 rvr.py
python3 server.py >> teleop
```
