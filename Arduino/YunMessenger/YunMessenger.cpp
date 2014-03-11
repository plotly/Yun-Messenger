#include "YunMessenger.h"
#include <Bridge.h>
#include <Console.h>

#include "Arduino.h"

Messenger::Messenger(){
    Console.buffer(64);
}

void Messenger::send(char *subscriber, char *message){
    Console.print(char(29));
    Console.print(subscriber);
    Console.print(char(30));
    Console.print(message);
    Console.print(char(31));
    Console.flush();
}