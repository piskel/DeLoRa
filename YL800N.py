import serial
import serial.tools.list_ports
import time

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
COM_AT_SADDR        = ['AT+SADDR',      ['{:04x}']]
COM_AT_CHANNEL      = ['AT+CHANNEL',    ['{:d}']]
COM_AT_PANID        = ['AT+PANID',      ['{:04x}']]
COM_AT_USERMODE     = ['AT+USERMODE',   ['{:d}']]
COM_AT_SEND         = ['AT+SEND',       ['{:x}', '"{}"']]


BCAST_ADDR = 0xFFFF



# Roles
ROLE_MASTER = 1
ROLE_SLAVE = 0

# Usermodes
USERMODE_HEX = 1
USERMODE_TRANSPARENT = 0
USERMODE_AT = 2

class YL800N:
    def __init__(self, com_port):
        self.__com_port = com_port
        self.__ser = serial.Serial(
            self.__com_port,
            9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        


    def get_com_port_list():
        return list(serial.tools.list_ports.comports())

    def open_communication(self):
        if not self.__ser.is_open:
            self.__ser.open()

    def close_communication(self):
        if self.__ser.is_open:
            self.__ser.close()

    def is_communication_open(self):
        return self.__ser.is_open


    def change_mode(self, mode):
        result = ""
        if mode == USERMODE_AT:
            result = self.feed_com(COM_SWITCH_TO_AT)
        else:
            result = self.feed_com(COM_AT_USERMODE, [mode])


    
    def is_input_buffer_empty(self):
        return self.__ser.in_waiting == 0


    def read_com(self):
        input_buffer = self.__ser.readline()
        return input_buffer


    def feed_com(self, command:COMType, args=[]):
        query_list = [command[0]]
        if len(args) > 0:
            if len(args) != len(command[1]):
                raise ValueError("Argument number mismatch")
            
            query_list.append(f','.join(command[1]).format(*args))
        query_str = ' '.join(query_list)

        if command != COM_SWITCH_TO_AT:
            query_str += '\r\n'
        
        self.__ser.write((query_str).encode())
        result = self.__ser.readline().decode()
        
        # Debug
        print('{} -> {}'.format(query_str.encode(), result.encode()))
        
        return result


    def safe_feed_com(self, command:COMType, args=[]):

        self.change_mode(USERMODE_AT)
        result = self.feed_com(command, args)
        self.change_mode(USERMODE_TRANSPARENT)
        return result
        

    @property
    def module_version(self):
        result = self.safe_feed_com(COM_AT_VERSION)
        return result[-7:-2]

    @property
    def role(self):
        result = self.safe_feed_com(COM_AT_ROLE)
        return int(result[-3:-2])

    @role.setter
    def role(self, role):
        self.safe_feed_com(COM_AT_ROLE, [role])


    @property
    def laddr(self):
        result = self.safe_feed_com(COM_AT_LADDR)
        return result[-19:-2]


    @property
    def saddr(self):
        result = self.safe_feed_com(COM_AT_SADDR)
        return int(result[-4:-2]+result[-6:-4], base=16)

    @saddr.setter
    def saddr(self, value):
        self.safe_feed_com(COM_AT_SADDR, [value])



    
    @property
    def channel(self):
        result = self.safe_feed_com(COM_AT_CHANNEL)
        return int(result[-4:-2])
    
    @channel.setter
    def channel(self, value):
        self.safe_feed_com(COM_AT_CHANNEL, [value])



    @property
    def panid(self):
        result = self.safe_feed_com(COM_AT_PANID)
        return int(result[-4:-2]+result[-6:-4], base=16)
    
    @panid.setter
    def panid(self, value):
        self.safe_feed_com(COM_AT_PANID, [value])


