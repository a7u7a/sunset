Run example with:

````
sudo python app.py --led-cols=128 --led-rows=32 --led-slowdown=2 --led-gpio-mapping=adafruit-hat
````

# Autostart setup
- Shh into the pi: $ ssh pi@raspberrypi.local
- Create unit file: $ sudo nano /lib/systemd/system/sunset.service
- Add this to the file:

````
[Unit]
Description=Sunset scroller daemon
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/sunset/
ExecStart=/usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/sunset/app.py --led-cols=96 --led-slowdown-gpio=5 --led-gpio-mapping=regular  --led-rows=48 --led-chain=1 --led-pixel-mapper=u-mapper --led-parallel=3 --led-brightness=70 --led-row-addr-type=3 --led-pwm-lsb-nanoseconds=50 --led-pwm-bits=7

[Install]
WantedBy=multi-user.target
````

- Reload daemons: `$ sudo systemctl daemon-reload`
- Enable service on boot: `$ sudo systemctl enable sunset.service`
- Reboot: `$ sudo reboot`


# Check that daemon is running

- Run: $ systemctl status sunset.service
- Output should be like:

````
pi@raspberrypi:~ $ systemctl status sunset.service
● sunset.service - Sunset scroller daemon
     Loaded: loaded (/lib/systemd/system/sunset.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2022-03-05 00:13:22 GMT; 10min ago
   Main PID: 955 (python3)
      Tasks: 7 (limit: 1597)
        CPU: 8min 32.862s
     CGroup: /system.slice/sunset.service
             └─955 /usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/sunset/app.py --led-cols=768...

Mar 05 00:13:22 raspberrypi systemd[1]: Started Sunset daemon.
Mar 05 00:13:24 raspberrypi python3[955]: Suggestion: to slightly improve display update, add
Mar 05 00:13:24 raspberrypi python3[955]:         isolcpus=3
Mar 05 00:13:24 raspberrypi python3[955]: at the end of /boot/cmdline.txt and reboot (see README.md)
````

# Stop daemon
Run $ service sunset stop