#!/usr/bin/python
# -*- coding: utf-8 -*-

from Event import Event
from SERIAL import SERIAL
from socket import socket, AF_INET, SOCK_STREAM
from Logger import Logger

import traceback
import time

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
            Logger.logger.error("Console.recv failed, closing connection")
            Logger.logger.debug("Traceback: {traceback}".format(traceback=traceback.format_exc()))
            self.console.close()
            self.connected = False
            return None

        # if new data was received then add it buffer and check if end message was provided
        if new_data:
            self.msg_buffer += new_data
            index_end = self.msg_buffer.find(SERIAL.MSG.END)

        if new_data == '':
            # client closed the connection
            Logger.logger.info("Socket connection closed")
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
                publish_route = self.msg_buffer[(index_name + 1):index_msg]
                msg = self.msg_buffer[(index_msg + 1):index_end]                
                try:
                    self.onMessage(publish_route, msg)
                except Exception:
                    Logger.logger.error("Publishing the following message "\
                                "to subscriber \"{subscriber}\" failed:\n{message}"\
                                .format(subscriber=publish_route, message=msg))
                    Logger.logger.debug("Traceback: \n{traceback}".format(traceback=traceback.format_exc()))

            self.msg_buffer = ""

    def run(self):
        self.console = socket(AF_INET, SOCK_STREAM)
        self.connected = False        

        while 1:
            if self.connected:
                self.read()
            else:
                try:
                    time.sleep(0.5)
                    self.Logger.logger.info("Attempting to connect to localhost:6571")
                    self.console.close()
                    self.console.connect(('localhost', 6571))
                    self.Logger.logger.info("Connected to localhost:6571")
                    self.connected = True
                except KeyboardInterrupt:
                    self.Logger.logger.info("KeyboardInterrupt, exiting")
                    break
                except:
                    self.Logger.logger.error("Can't connect to localhost:6571")
