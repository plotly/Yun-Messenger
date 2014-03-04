# Set up a socket client that mimics the Arduino Messenger
import socket

from Linino import Console

HOST = 'localhost'
PORT = 6575

class ArduinoMessengerMimic:
    def __init__(self):
        self.start()

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))        

    def send(self, subscriber, msg):
        self.sock.send(Console.SERIAL.MSG.NAME)
        self.sock.send(subscriber)
        self.sock.send(Console.SERIAL.MSG.DATA)
        self.sock.send(msg)
        self.sock.send(Console.SERIAL.MSG.END)

    def close(self):
        self.close = self.sock.close()

messenger = ArduinoMessengerMimic()
messenger.start()
messenger.send('subscriber1', 'Hello subscriber 1')
messenger.send('subscriber2', 'Hello subscriber 2')
messenger.send('doesnotexist', 'Talking to no one')
messenger.send('brokenSubscriber', 'call me ishmael')
messenger.close()

messenger.start()
messenger.send('subscriber1', 'Hello again subscriber 1')
messenger.send('subscriber2', 'Hello again subscriber 2')
messenger.close()