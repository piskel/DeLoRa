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
COM_AT_SEND         = ['AT+SEND',       ['{:04x}', '"{}"']]


BCAST_ADDR = 0xFFFF


# Roles
ROLE_MASTER = 1
ROLE_SLAVE = 0

# Usermodes
USERMODE_HEX = 0
USERMODE_TRANSPARENT = 1
USERMODE_AT = 2

# Baudrates
BAUD_1200 = 1
BAUD_2400 = 2
BAUD_4800 = 3
BAUD_9600 = 4
BAUD_14400 = 5
BAUD_19200 = 6
BAUD_28800 = 7
BAUD_38400 = 8
BAUD_57600 = 9
BAUD_76800 = 10
BAUD_115200 = 11
BAUD_230400 = 12

# UART Parameters
UART_PARAM1_1_STOP_BIT = 0
UART_PARAM1_2_STOP_BIT = 1

UART_PARAM2_NO_PARITY = 0
UART_PARAM2_ODD_PARITY = 1
UART_PARAM2_EVEN_PARITY = 2


class YL800N:
    def __init__(self, com_port):
        self.__com_port = com_port
        self.__ser = serial.Serial(
            self.__com_port.device,
            9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        
        # self._baudrate = BAUD_9600

        


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
        result = self.__ser.readline()
        
        # Debug
        print('{} -> {}'.format(query_str, result))
        
        return result


    def safe_feed_com(self, command:COMType, args=[]):
        self.change_mode(USERMODE_AT)
        result = self.feed_com(command, args)
        self.change_mode(USERMODE_TRANSPARENT)
        return result


    def send_data(self, data, addr=BCAST_ADDR):
        data = data.encode()
        data_encoded = ''.join(format(x, '02x') for x in data)
        self.safe_feed_com(COM_AT_SEND, [addr, data_encoded])


    def restore_defaults(self):
        self.safe_feed_com(COM_AT_DEFAULT)
    
    
    def reset(self):
        self.safe_feed_com(COM_AT_RESET)


    @property
    def module_version(self):
        result = self.safe_feed_com(COM_AT_VERSION)
        return result[-7:-2]
    
    @property
    def baudrate(self):
        result = self.safe_feed_com(COM_AT_BAUD)
        return int(result[-3:-2], 16)

    @baudrate.setter
    def baudrate(self, baudrate):
        self.safe_feed_com(COM_AT_BAUD, [baudrate])


    @property
    def uart_parity(self):
        result = self.safe_feed_com(COM_AT_UARTPARA)
        return [int(result[-5:-4]), int(result[-3:-2])]
    
    @uart_parity.setter
    def uart_parity(self, parity):
        self.safe_feed_com(COM_AT_UARTPARA, [parity[0], parity[1]])

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






