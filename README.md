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
    ```

    And that's it! You've successfully communicated a message between your Yún and a Python program on your Linino. 

### Running the messenger in the background
You can start your Python program from your Yún with the `Process` module:
```C
void setup(){
    Process.run("python ~/example.py");
}
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
[...]
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
