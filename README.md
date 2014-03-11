## Yun-Messenger

Communicate messages from the Arduino ATmega32u4 microcontroller to Python programs on the Linino.

It's as simple as:

```C
#include <Messenger.h>

void setup(){
    Messenger.send("my_subscriber", "my message contents");
}
```

and in Python on the Linino:
```python
import yunMessenger

ym = yunMessenger()

ym.onMessage['my_subscriber'] = myMessageHandler

def myMessageHandler(msg):
    print msg

```

Or, with multiple subscribers
```C
#include <Messenger.h>

void setup(){
    Messenger.send("subscriber_1", "my message contents");
    Messenger.send("subscriber_2", "my message contents");
}
```

```python
import yunMessenger

ym = yunMessenger()

ym.onMessage['subscriber_1'] = messageHandler1
ym.onMessage['subscriber_1'] = messageHandler2

def messageHandler1(msg):
    print 'Handler 1! ', msg

def messageHandler2(msg):
    print 'Handler 2! ', msg


```


## Credits
The Console object adapted from [Spacebrew's awesome project](https://github.com/julioterra/yunSpacebrew)
