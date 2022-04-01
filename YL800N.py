import serial

# TODO: Enum pour les roles

class YL800N:
    def __init__(self, mode, saddr, com_port):
        self.mode = mode # 1: master, 0: slave
        self.saddr = saddr
        self.com_port = com_port
        self.ser = serial.Serial(
            self.com_port,
            9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

    def open_com(self):
        if not self.ser.is_open:
            self.ser.open()

    def close_com(self):
        if self.ser.is_open:
            self.ser.close()

    def feed_com(self, data):
        self.ser.write(data.encode())
        return self.ser.readline().decode()

    def get_version(self):
        return self.feed_com('AT+VERSION\r\n')






    def configure(self):
        self.feed_com('+++')
        self.feed_com('AT+ROLE {}\r\n'.format(self.mode))
        self.feed_com('AT+SADDR {}\r\n'.format(self.saddr))
        self.feed_com('AT+USERMODE 1\r\n') # Return to transparent mode
        print(self.ser.readline())

    def send_message(self, dest_addr, message):
        pass