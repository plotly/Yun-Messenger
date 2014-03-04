#!/usr/bin/python

from Event import Event
from socket import socket, AF_INET, SOCK_STREAM

class SERIAL:
    class MSG:
        NAME            = chr(29)
        DATA            = chr(30)
        END             = chr(31)


class Console(object):
    pass

    def __init__(self):
        self.connected = False
        self.msg_buffer = ""

        # Events
        self.onMessage = Event()

    def read(self):
        if not self.connected: return None
        index_end = -1

        # wait here for messages
        try:
            new_data = self.console.recv(1024)
        except:
            self.connected = False
            return None

        # if new data was received then add it buffer and check if end message was provided
        if new_data:
            print new_data
            self.msg_buffer += new_data
            index_end = self.msg_buffer.find(SERIAL.MSG.END)

        if new_data == '':
            # client closed the connection
            print 'closing'
            self.console.close()
            self.connected = False
            return None

        # if message end was found, then look for the start and div marker
        if index_end > 0:
            index_name = self.msg_buffer.find(SERIAL.MSG.NAME)
            index_msg = self.msg_buffer.find(SERIAL.MSG.DATA)

            publish_route = "" 
            msg = ""

            if index_name >= 0 and index_msg > index_name:
                print 'Found index markers'
                publish_route = self.msg_buffer[(index_name + 1):index_msg]
                msg = self.msg_buffer[(index_msg + 1):index_end]
                print 'publish_route:', publish_route, 'msg:', msg
                
                try:
                    self.onMessage(publish_route, msg)
                except Exception:
                    error_msg = "issue sending message, route: " + publish_route + "\n"
                    self.log(error_msg)

            self.msg_buffer = ""

    def run(self):
        while 1:
            if self.connected:
                self.read()
            else:
                self.console = socket(AF_INET, SOCK_STREAM)
                self.console.bind(('localhost', 6571))
                self.console.listen(1)
                self.connected = True

    def log(self, message):
        # TODO: user defined loggers
        print message
