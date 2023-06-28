Run example with:

````
sudo python app.py --led-cols=128 --led-rows=32 --led-slowdown=2 --led-gpio-mapping=adafruit-hat
````

# Autostart setup: Debt Scroller display
- Shh into the pi: $ ssh pi@raspberrypi.local
- Create unit file: $ sudo nano /lib/systemd/system/sunset.service
- Add this to the file:

````
[Unit]
Description=Sunset scroller daemon
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/
ExecStart=/usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/sunset/app.py --led-cols=96 --led-slowdown-gpio=5 --led-gpio-mapping=regular  --led-rows=48 --led-chain=1 --led-pixel-mapper=u-mapper --led-parallel=3 --led-brightness=70 --led-row-addr-type=3 --led-pwm-lsb-nanoseconds=50 --led-pwm-bits=7

[Install]
WantedBy=multi-user.target
````

Reload daemons: `$ sudo systemctl daemon-reload`
Enable service on boot: `$ sudo systemctl enable sunset.service`
Reboot: `$ sudo reboot`
