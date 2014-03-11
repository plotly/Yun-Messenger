#include <Bridge.h>
#include <Console.h>
#include <FileIO.h>
#include <HttpClient.h>
#include <Mailbox.h>
#include <Process.h>
#include <YunClient.h>
#include <YunServer.h>

#include <YunMessenger.h>

void setup() { 
    '''
    Console.buffer(64);
    Console.begin();
    Console.print(char(29));
    Console.print("my subscriber");
    Console.print(char(30));
    Console.print("my messenger");
    Console.print(char(31));
    Console.flush();
    '''
    
    //Messenger Messenger;
    //Messenger.send("my_subscriber", "my message contents");
}

void loop() { 

}