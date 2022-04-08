import serial

COMType = [str, [str]]

COM_SWITCH_TO_AT    = ["+++",           []]
COM_AT              = ['AT',            []]
COM_AT_VERSION      = ['AT+VERSION',    []]
COM_AT_DEFAULT      = ['AT+DEFAULT',    []]
COM_AT_RESET        = ['AT+RESET',      []]
COM_AT_BAUD         = ['AT+BAUD',       ['{:X}']]
COM_AT_UARTPARA     = ['AT+UARTPARA',   ['{:d}','{:d}']]
COM_AT_ROLE         = ['AT+ROLE',       ['{:d}']]
COM_AT_LADDR        = ['AT+LADDR',      []]
COM_AT_SADDR        = ['AT+SADDR',      ['{:x}']]
COM_AT_CHANNEL      = ['AT+CHANNEL',    ['{:d}']]
COM_AT_PANID        = ['AT+PANID',      ['{:x}']]
COM_AT_USERMODE     = ['AT+USERMODE',   ['{:d}']]
COM_AT_SEND         = ['AT+SEND',       ['{:x}', '"{}"']]


BCAST_ADDR = 0xFFFF

# Roles
ROLE_MASTER = 1
ROLE_SLAVE = 0

# Usermodes
USERMODE_HEX = 0
USERMODE_TRANSPARENT = 1
USERMODE_AT = 2

class YL800N:
    def __init__(self, com_port):
        self.com_port = com_port
        self.ser = serial.Serial(
            self.com_port,
            9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

    def open_communication(self):
        if not self.ser.is_open:
            self.ser.open()

    def close_communication(self):
        if self.ser.is_open:
            self.ser.close()

    def feed_com(self, com:COMType, args=[]):
        query_list = [com[0]]
        if len(args) > 0:
            if len(args) != len(com[1]):
                raise ValueError('Arguments do not match the number of arguments expected')
            
            query_list.append(f','.join(com[1]).format(*args))  # TODO: Change, not clean
        query_str = ' '.join(query_list)
        print(*args)
        print(query_str)
        self.ser.write((query_str+"\r\n").encode())
        return self.ser.readline()

