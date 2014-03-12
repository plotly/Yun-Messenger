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

    // Send Message to subscriber "subscriber_1"
    Messenger.send("subscriber_1", "Hey subscriber_1!");
    Messenger.send("subscriber_2", "Hey subscriber_2!");

    // You can also "open" a message, write to it, then close it
    // Anything that you write to the Console after you've 
    // opened the message will get sent to the Linino
    // and read by your Linino subscriber:
    Messenger.open("subscriber_1");
    Console.print("Hey subscriber");
    Console.print("_");
    Console.print(1);
    Console.print("!");
    Message.close();
}
