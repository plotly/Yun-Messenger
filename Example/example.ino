#include <Bridge.h>
#include <Console.h>
#include <YunMessenger.h>

void setup() { 

    // start-up the bridge
    Bridge.begin();

    delay(2000);
    Console.begin();
    while (!Console) {
      ; // wait for Console port to connect.
    }
    
    Console.buffer(64);
    delay(2000);    


    YunMessenger ym;
    // Send Message to subscriber "subscriber_1"
    ym.send("subscriber_1", "Hey subscriber_1!");
    ym.send("subscriber_2", "Hey subscriber_2!");
}