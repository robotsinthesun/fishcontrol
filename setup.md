[alternative manual install](https://www.raspberrypi.org/forums/viewtopic.php?t=121013)
[alternative manual install 2](https://kivy.org/docs/installation/installation-rpi.html)



## Basic setup
This is the screen: [3.5" LCD](https://www.waveshare.com/3.5inch-rpi-lcd-a.htm)
### Prepare SD card
#### Kivypie
* Download kivypie image

* Unzip

* Copy to SD of min size 4 GB using dd

#### LCD driver
* Download LCD driver from waveshare

* Unzip and place in /home/sysop on sd card

#### Set wifi credentials
Modify /boot/interfaces to setup wifi to match your ssid and password




### start raspi
* connect lcd, hdmi screen and keyboard to raspi

* log in using *sysop* and *posys* as user name and password
	* if you don't have a *QUERTY* keyboard layout, beware that y and z are swapped
	We will fix that later...

#### Test wifi connection.
ping *[your routers ip]*

If it fails:
* check your wifi credentials (see above)
* sudo ifdown wlan0
* sudo ifup wlan0

#### Update.
sudo apt-get update

sudo apt-get upgrade

#### Run sudo raspi-config
* Update this tool

* Advanced &rarr; Expand file system

* Change keyboard layout if needed
	* Localization &rarr; Change keyboard layout &rarr; Select 105 intel &rarr; Select "other", then scroll to whichever you need




#### Activate LCD screen.
see (waveshare instructions for more info)[foo]
cd into /home/sysop/LCD-show

chmod +x LCD35-show
./ LCD35-show


This will restart the Pi.


### Get Kivy to work on the 3.5" LCD.
Usually, to set the screen Kivy will display on, we should set an environment variable like this:

BCM_
The most helpful site was [this](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=145336).

#### Install frame buffer mirror
We need this guy because Kivy will only output to hdmi or the standard raspberry pi touch screen
cd ~
sudo apt-get install cmake
git clone https://github.com/tasanakorn/rpi-fbcp
cd rpi-fbcp/
mkdir build
cd build/
cmake ..
make
sudo install fbcp /usr/local/bin/fbcp

See [here](https://github.com/notro/fbtft/wiki/Framebuffer-use) and [here](https://github.com/tasanakorn/rpi-fbcp) for more info


#### Set touch rotation
nano ~/.kivy/config.ini
Comment lines under mouse and add
*stmpe-ts = hidinput,/dev/input/event0,rotation=270*
It might be necessary to change to event1, 2, 3 or 4...



