#ifndef YUNMESSENGER_H
#define YUNMESSENGER_H

#include <Bridge.h>
#include <Console.h>

#include "Arduino.h"

class Messenger {
    public:
        Messenger();
        void send(char *subscriber, char *message);
};

#endif