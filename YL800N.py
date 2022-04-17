import serial
import serial.tools.list_ports

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
        
        self._saddr = 0
        self._panid = 0

        self._current_mode = USERMODE_TRANSPARENT


    def get_com_port_list():
        return list(serial.tools.list_ports.comports())

    def open_communication(self):
        if not self.ser.is_open:
            self.ser.open()

    def close_communication(self):
        if self.ser.is_open:
            self.ser.close()

    # # Property accessor
    # @property
    # def saddr(self):
    #     return self._saddr

    # @saddr.setter
    # def saddr(self, value):
    #     self._saddr = value if value < 0xFFFF else 0xFFFF

    # @property
    # def panid(self):
    #     return self._panid

    # @panid.setter
    # def panid(self, value):
    #     self._panid = value if value < 32 else 0xFFFF

    # @property
    # def module_version(self):
    #     return self.feed_com(COM_AT_VERSION)[:-2].decode()



    def change_mode(self, mode):
        if mode != USERMODE_TRANSPARENT:
            self.feed_com(COM_AT_USERMODE, [mode])
            self._current_mode = mode
        
        # TODO: Check the changes were applied



    def is_input_buffer_empty(self):
        return self.ser.in_waiting == 0

    def read_com(self):
        input_buffer = self.ser.readline()
        # self.ser.reset_input_buffer()
        return input_buffer


    def feed_com(self, com:COMType, args=[]):
        query_list = [com[0]]
        if len(args) > 0:
            if len(args) != len(com[1]):
                raise ValueError("Argument number mismatch")
            
            query_list.append(f','.join(com[1]).format(*args))
        query_str = ' '.join(query_list)
        
        
        self.ser.write((query_str).encode())
        return self.ser.readline()

