## YunMessenger

Arduino's `Bridge` abstraction opens up communication between the Yún and the Linino, but using it in your Python programs on the Linino is a ton of work: you have to set up TCP sockets and parse streaming data. And since all of the communication between processors is over the same TCP socket on port 6571 on `localhost`, multiple subscribers can't tune in if they don't know which message is for whom.

It shouldn't be this hard, not on the Arduino.

The YunMessenger simplifies communication from the Arduino ATmega32u4 microcontroller to Python programs on the Linino.

It's as simple as:

```C
#include <YunMessenger.h>

void setup(){
    Messenger m;
    m.send("my_subscriber", "my message contents");
}
```

and in your Python on the Linino:
```python
from YunMessenger import Console

console = Console.Console()

def myMessageHandler(msg):
    print msg

console.onMessage['my_subscriber'] = myMessageHandler

console.run()
```

Or, with multiple subscribers
```C
#include <YunMessenger.h>

void setup(){
    Messenger m;
    m.send("subscriber_1", "Hey subscriber_1!");
    m.send("subscriber_2", "Hey subscriber_2!");
}
```

```python
from YunMessenger import Console

console = Console.Console()

def messageHandler1(msg):
    print 'Handler 1! ', msg

def messageHandler2(msg):
    print 'Handler 2! ', msg

console.onMessage['subscriber_1'] = messageHandler1
console.onMessage['subscriber_2'] = messageHandler2

console.run()
```

It was developed for [Plotly's real-time plotting library on the Yún](https://github.com/plotly/arduino-api/tree/master/plotly_yun).

## Getting Started

1. Connect to your Yún to your local network
2. Download this repository
3. Copy the YunMessenger folder and the example script to your Linino. In your terminal, enter:
    ```bash
    $ scp -r Linino/* root@arduino.local:YunMessenger/
    $ scp example.py root@arduino.local:/root/
    ```

4. Add the YunMessenger folder in this repository's Arduino folder to your Arduino libraries. On a mac, this is located in ~/Documents/Arduino/Libraries:
![Library Screenshot](http://new.tinygrab.com/c751bc2ee24070065bd90b492004598213e5197dd2.png)
5. Restart the [latest Arduino IDE](http://arduino.cc/en/main/software)
6. Run example.ino from this file
7. SSH in to your arduino and run example.py and observer the output
    ```bash
    $ ssh root@arduino.local
    [...]
    root@Arduino:~# python example.py
    Handler 1!  Hey subscriber_1!
    Handler 2!  Hey subscriber_2!
    ```

    And that's it! You've successfully communicated a message between your Yún and a Python program on your Linino. 

### Running the messenger in the background
You can run processes in the background by appending `&` to your bash commands:
```bash
root@Arduino:~# (python example.py)&
```

Observer which processes are running with `top`:
```bash
root@Arduino:~# top

Mem: 53728K used, 7404K free, 0K shrd, 5256K buff, 18404K cached
CPU:   0% usr   9% sys   0% nic  90% idle   0% io   0% irq   0% sirq
Load average: 0.39 0.35 0.33 1/52 14213
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
14213 13667 root     R     1500   2%   9% top
13705 13667 root     S    13924  23%   0% python example.py
 1530     1 nobody   S     2180   4%   0% avahi-daemon: running [Arduino.local]
 1502     1 root     S     1700   3%   0% /usr/sbin/dbus-daemon --system
 1167     1 root     S     1588   3%   0% wpa_supplicant -B -P /var/run/wifi-wl
 1493     1 root     S     1576   3%   0% /usr/sbin/uhttpd -f -h /www -r Arduin
  574     1 root     S     1552   3%   0% {rcS} /bin/sh /etc/init.d/rcS S boot
  731     1 root     S     1540   3%   0% /sbin/netifd
  701     1 root     S     1512   2%   0% /sbin/syslogd -C16
 1251   731 root     S     1512   2%   0% udhcpc -p /var/run/udhcpc-wlan0.pid -
 1565     1 root     S N   1508   2%   0% {uSDaemon} /bin/sh /sbin/uSDaemon
    1     0 root     S     1508   2%   0% init
13667 13655 root     S     1508   2%   0% -ash
13352 13335 root     S     1508   2%   0% -ash
11639     1 root     S     1504   2%   0% /bin/ash --login
  788   731 root     S     1504   2%   0% udhcpc -p /var/run/udhcpc-eth1.pid -s
13369 13352 root     S     1504   2%   0% top
 1556     1 root     S     1504   2%   0% /usr/sbin/ntpd -n -p 0.openwrt.pool.n
  845     1 root     S     1504   2%   0% /sbin/watchdog -t 5 /dev/watchdog
```

Kill these background processes with:
```bash
root@Arduino:~# kill -9 $(pgrep -f "python example.py")
```
    


### Debugging and Logging
On the Linino, status updates, warnings, and errors are written to a file called `YunMessenger.log`. This file is capped at 0.5MB. 
```bash
root@Arduino:~# cat YunMessenger.log
[...]
```
The file might have a ton of lines and be overwhelming to look at. To check out just the last 50 lines, try:
```
root@Arduino:~# tail -n100 YunMessenger.log
[...]
```
To watch the messages as they're being written to the file in real time, try:
```
root@Arduino:~# tail -f YunMessenger.log

2014-03-12 01:35:35 INFO: Attempting to connect to localhost:6571
2014-03-12 01:35:35 ERROR: Can't connect to localhost:6571
2014-03-12 01:35:35 DEBUG: Traceback (most recent call last):
  File "/root/YunMessenger/Console.py", line 83, in run
    self.console.connect(('localhost', 6571))
  File "/usr/lib/python2.7/socket.py", line 224, in meth
    return getattr(self._sock,name)(*args)
error: [Errno 146] Connection refused

2014-03-12 01:35:36 INFO: Attempting to connect to localhost:6571
2014-03-12 01:35:36 INFO: Connected to localhost:6571
```

## How does this work?

The Arduino microcontroller (ATmega32u4) sends data to the Linino over the `bridge`. The `bridge` is just a TCP connection over port `6571` on `localhost`. This library defines a basic communication protocal over this TCP connection where messages must are sent in the format:
```
char(29) subscriber_name char(30) message char(31)
```

On the Arduino side, the communication over this socket looks like:
```C
#include <Bridge.h>
#include <Console.h>

Bridge.begin();
Console.begin();
while (!Console) {
  ; // wait for Console port to connect.
}

Console.print(char(29)); // indicate the start of the subscriber name
Console.print("plotly"); // the name of the subscriber
Console.print(char(30)); // indicates the start of the message
Console.print("{\"x\": 1, \"y\": 10}"); // the message (in this case a JSON object)
Console.print(char(31)); // indicates the end of the message
```
On the Linino side, `YunMessenger.Console` opens a TCP socket on port `6571` of `localhost`, parses the messages, and calls the associated subscriber's event handlers (if any).


## Credits
The TCP protocal was adapted from [Spacebrew's awesome project](https://github.com/julioterra/yunSpacebrew/). Check them out!
