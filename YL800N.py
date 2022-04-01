import serial





# Roles
ROLE_MASTER = 1
ROLE_SLAVE = 0

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
        self.ser.write((data+"\r\n").encode())
        return self.ser.readline()


    def get_version(self):
        return self.feed_com('AT+VERSION')




    def configure(self):
        self.feed_com('+++')
        self.feed_com('AT+ROLE {}'.format(self.mode))
        self.feed_com('AT+SADDR {}'.format(self.saddr))
        self.feed_com('AT+USERMODE 1') # Return to transparent mode
        print(self.ser.readline())

    def send_message(self, dest_addr, message):
        self.feed_com('+++')
        # Convert message to hex
        message = message.encode()
        message_hex = ''.join(format(x, '02x') for x in message)
        print('AT+SEND {},"{}"'.format(dest_addr, message_hex))
        self.feed_com('AT+SEND {},"{}"'.format(dest_addr, message_hex))
        