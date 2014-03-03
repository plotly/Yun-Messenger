class SERIAL:
    class MSG:
        NAME            = chr(29)
        DATA            = chr(30)
        END             = chr(31)
        CONFIRM         = chr(7)

    class CONNECTION:
        START           = chr(28)
        END             = chr(27)
        ERROR           = chr(26)


class Console(object):
    pass

    def __init__(self, brew):
        self.console = socket(AF_INET, SOCK_STREAM)
        self.connected = False
        self.msg_buffer = ""

        # Events
        self.onMessage = Event()

    def start(self):
        try:
            self.console = socket(AF_INET, SOCK_STREAM)
            self.console.connect(('localhost', 6571))
            self.connected = True

        except:
            self.connected = False

    def read(self):
        if not self.connected: return

        index_end = -1

        new_data = self.console.recv(1024)

        # if new data was received then add it buffer and check if end message was provided
        if new_data:
            self.msg_buffer += new_data
            index_end = self.msg_buffer.find(SERIAL.MSG.END)

        if new_data == '':
            console_running = False
            self.console.close()
            return None

        # if message end was found, then look for the start and div marker
        if index_end > 0:
            index_name = self.msg_buffer.find(SERIAL.MSG.NAME)
            index_msg = self.msg_buffer.find(SERIAL.MSG.DATA)

            publish_route = "" 
            msg = ""

            if index_name >= 0 and index_msg > index_name:

                try:
                    publish_route = self.msg_buffer[(index_name + 1):index_msg]
                    msg = self.msg_buffer[(index_msg + 1):index_end]
                    self.onMessage(publish_route, msg)

                except Exception:
                    error_msg = "issue sending message via spacebrew, route: " + publish_route + "\n"
                    self.log(error_msg)

                try:
                    confirm_pub = SERIAL.MSG.CONFIRM + publish_route + SERIAL.MSG.END
                    self.log(confirm_pub)

                except Exception:
                    error_msg = "issue sending confirmation about: " + publish_route + "\n"
                    self.log(error_msg)

            self.msg_buffer = ""

    def run(self):
        self.start()
        try:
            while True:
                if self.connected: 
                    self.read()
        finally:
            self.console.close()

    def publish(self, name, message):
        try:
            full_msg = SERIAL.MSG.NAME + name + SERIAL.MSG.DATA + message + SERIAL.MSG.END
            self.console.send(full_msg)
        except:
            pass

    def log(self, message):
        self.console.send(message)
