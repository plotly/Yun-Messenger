# Set up a socket client that mimics the Arduino Messenger
import socket

import Console
import config

class Messenger(object):
    def __init__(self):
        pass

    def start(self):
        self.socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((config.HOST, config.PORT))        

    def send(self, subscriber, msg):
        self.send(Console.SERIAL.NAME)
        self.send(subscriber)
        self.send(Console.SERIAL.DATA)
        self.send(msg)

    def close(self):
        self.close = self.socket.close()

messenger = Messenger()
messenger.send('subscriber1', 'Hello subscriber 1')
messenger.send('subscriber2', 'Hello subscriber 2')
messenger.send('doesnotexist', 'Talking to no one')
messenger.send('brokenSubscriber', 'call me ishmael')
messenger.close()

messenger = Messenger()
messenger.send('subscriber1', 'Hello again subscriber 1')
messenger.send('subscriber2', 'Hello again subscriber 2')
messenger.close()