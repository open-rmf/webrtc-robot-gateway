# webrtc-robot-gateway

## Installation Instructions

### Setup
```
# Install Ubuntu 21.04 with Desktop on Rpi4
https://ubuntu.com/download/raspberry-pi

apt update && apt upgrade
apt install avahi-daemon openssh-server
```

### Set up DroidCam if using Android Phone for Camera
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

## Install aiortc
apt install libavdevice-dev libavfilter-dev libopus-dev libvpx-dev pkg-config python3-pip
pip3 install aiortc aiohttp
cd; git clone https://github.com/aiortc/aiortc.git
```

