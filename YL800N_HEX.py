from netrc import netrc
import serial.tools.list_ports
import time
from struct import *
from enum import Enum
from typing import Union


class SERIAL_PARAMETERS:
    class BAUDRATE(Enum):
        BAUDRATE_1200 = 1
        BAUDRATE_2400 = 2
        BAUDRATE_4800 = 3
        BAUDRATE_9600 = 4
        BAUDRATE_14400 = 5
        BAUDRATE_19200 = 6
        BAUDRATE_28800 = 7
        BAUDRATE_38400 = 8
        BAUDRATE_57600 = 9
        BAUDRATE_76800 = 10
        BAUDRATE_115200 = 11
        BAUDRATE_230400 = 12

    class PARITY(Enum):
        PARITY_NONE = 0
        PARITY_ODD = 1
        PARITY_EVEN = 2

    class STOP_BIT(Enum):
        STOP_BIT_1 = 0
        STOP_BIT_2 = 1

    def __init__(self,
        baudrate: BAUDRATE,
        parity: PARITY,
        stopbits: STOP_BIT):

        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits

    def value(self) -> int:
        return self.baudrate.value << 4 | self.parity.value << 1 | self.stopbits.value


class FRAME_MODULE_CONFIG:
    CONFIG_FLAG = [0xA5, 0xA5]

    class CHANNEL(Enum):
        CH431M = 0
        CH432M = 1 # Default
        CH429M = 2
        CH433M = 3
        CH436M = 4
        CH434M = 5
        CH437M = 6
        CH435M = 7

    class TX_POWER(Enum):
        PWR20dBm = 0 # Default
        PWR17dBm = 1
        PWR15dBm = 2
        PWR13dBm = 3
        PWR11dBm = 4
        PWR9dBm = 5
        PWR7dBm = 6
        PWR5dBm = 7

    class USER_MODE(Enum):
        HEXADECIMAL = 0 # Default
        TRANSPARENT = 1

    class ROLE(Enum):
        SLAVE = 0 # Default
        MASTER = 1

    def __init__(self,
        channel: CHANNEL,
        user_mode: USER_MODE,
        role: ROLE,
        network_flag,
        node_flag,
        serial_parameters: SERIAL_PARAMETERS,
        tx_power:TX_POWER=TX_POWER.PWR20dBm,
        bandwidth=9,
        spread_factor=9):

        self.channel = channel
        self.tx_power = tx_power
        self.user_mode = user_mode
        self.role = role
        self.network_flag = network_flag
        self.node_flag = node_flag
        self.serial_parameters = serial_parameters
        self.bandwidth = bandwidth
        self.spread_factor = spread_factor

    def value(self) -> bytes:
        result = bytearray()
        result.extend(self.CONFIG_FLAG)
        result.append(self.channel)
        result.append(self.tx_power.value)
        result.append(self.user_mode.value)
        result.append(self.role.value)
        network_flag_reversed = pack('>H', self.network_flag)
        network_flag_reversed = network_flag_reversed[::-1]
        result.extend(network_flag_reversed)
        node_flag_reversed = pack('>H', self.node_flag)
        node_flag_reversed = node_flag_reversed[::-1]
        result.extend(node_flag_reversed)
        result.extend([0x00, 0x00, 0x02])
        result.append(self.serial_parameters.value())
        result.append(self.bandwidth)
        result.append(self.spread_factor)
        return result


class FRAME_APPLICATION_DATA:
    class WAIT_ACK(Enum):
        DISABLED = 0x00
        ENABLED = 0x01

    class ROUTE_DISCOVERY(Enum):
        DISABLED = 0x00
        AUTOMATIC = 0x01
        FORCED = 0x02
        # SOURCE = 0x03 # Not supported

    def __init__(self,
        target_address,
        wait_ack: WAIT_ACK,
        max_hops,
        route_discovery: ROUTE_DISCOVERY,
        payload: bytes):

        self.target_address = target_address
        self.wait_ack = wait_ack
        self.send_radius = max_hops
        self.route_discovery = route_discovery
        self.payload_length = len(payload)
        self.payload = payload

    def value(self):
        result = bytearray()
        target_address_reversed = pack('>H', self.target_address)
        target_address_reversed = target_address_reversed[::-1]
        result.extend(target_address_reversed)
        result.append(self.wait_ack.value)
        result.append(self.max_hops)
        result.append(self.route_discovery.value)
        result.append(self.payload_length)
        result.extend(self.payload)
        return result


class FRAME:

    class FRAME_TYPE(Enum):
        MODULE_CONFIG = 0x01
        MAC_TESTING = 0x02
        NET_TESTING = 0x03
        DEBUG = 0x04
        APPLICATION_DATA = 0x05

    SEQUENCE_NUMBER = 0x00

    class COMMAND_TYPE:
        COMMAND_TYPE_RESPONSE = 0x80

        class MODULE_CONFIG(Enum):
            WRITE_CONFIG = 0x01
            READ_CONFIG = 0x02
            VERSION = 0x06
            RESET = 0x07

        class DEBUG(Enum):
            WRITE_ACCESS_CONTROL_LIST = 0x01
            READ_ACCESS_CONTROL_LIST = 0x02

        class APPLICATION_DATA(Enum):
            SEND = 0x01
            RECEIVE = 0x02
            ROUTE_DISCOVERY = 0x08

    def __init__(self,
        frame_type: FRAME_TYPE,
        command_type: Union[COMMAND_TYPE.MODULE_CONFIG, COMMAND_TYPE.DEBUG, COMMAND_TYPE.APPLICATION_DATA],
        payload: bytes):

        self.frame_type = frame_type
        self.command_type = command_type
        self.payload = payload

    def value(self) -> bytes:
        result = bytearray()
        result.append(self.frame_type.value)
        result.append(self.SEQUENCE_NUMBER)
        result.append(self.command_type.value)
        result.append(len(self.payload))
        result.extend(self.payload)
        crc = 0
        for b in result:
            crc = crc ^ b
        result.append(crc)

        return result


# TODO: Update serial interface to both module and client when changing them

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
    
    def send_frame(self, frame:FRAME):
        self.__ser.write(frame.value())
        result = self.__ser.readline()

        # Debug
        print("Sent : ", end='')
        for b in frame.value():
            print("{:02x}".format(b), end = " ")
        
        print("\nReceived : ", end='')
        for b in result:
            print("{:02x}".format(b), end = " ")


    def set_config(self,
        channel: FRAME_MODULE_CONFIG.CHANNEL,
        user_mode: FRAME_MODULE_CONFIG.USER_MODE,
        role: FRAME_MODULE_CONFIG.ROLE,
        network_flag,
        node_flag,
        tx_power: FRAME_MODULE_CONFIG.TX_POWER = FRAME_MODULE_CONFIG.TX_POWER.PWR20dBm,
        bandwidth=9,
        spread_factor=9):
        serial_parameters = SERIAL_PARAMETERS(
            SERIAL_PARAMETERS.BAUDRATE.BAUDRATE_9600,
            SERIAL_PARAMETERS.PARITY.PARITY_NONE,
            SERIAL_PARAMETERS.STOP_BIT.STOP_BIT_1)

        frame = FRAME(
            FRAME.FRAME_TYPE.MODULE_CONFIG,
            FRAME.COMMAND_TYPE.MODULE_CONFIG.WRITE_CONFIG,
            FRAME_MODULE_CONFIG(
                channel,
                tx_power,
                user_mode,
                role,
                network_flag,
                node_flag,
                serial_parameters,
                bandwidth,
                spread_factor).value())
        
        self.send_frame(frame)


    
    def send_data(self,
        target_address,
        payload:bytes,
        wait_ack: FRAME_APPLICATION_DATA.WAIT_ACK = FRAME_APPLICATION_DATA.WAIT_ACK.DISABLED,
        max_hops=7,
        route_discovery: FRAME_APPLICATION_DATA.ROUTE_DISCOVERY = FRAME_APPLICATION_DATA.ROUTE_DISCOVERY.AUTOMATIC
        ):
        frame = FRAME(
            FRAME.FRAME_TYPE.APPLICATION_DATA,
            FRAME.COMMAND_TYPE.APPLICATION_DATA.SEND,
            FRAME_APPLICATION_DATA(
                target_address,
                wait_ack,
                max_hops,
                route_discovery,
                payload).value())
    
        self.send_frame(frame)



# ser_conf = SERIAL_PARAMETERS(
#     SERIAL_PARAMETERS.BAUDRATE.BAUDRATE_9600,
#     SERIAL_PARAMETERS.PARITY.PARITY_NONE,
#     SERIAL_PARAMETERS.STOP_BIT.STOP_BIT_1)



# test=FRAME_MODULE_CONFIG(
#     FRAME_MODULE_CONFIG.CHANNEL.CH432M,
#     FRAME_MODULE_CONFIG.TX_POWER.PWR20dBm,
#     FRAME_MODULE_CONFIG.USER_MODE.HEXADECIMAL,
#     FRAME_MODULE_CONFIG.ROLE.SLAVE,
#     0x03,
#     0x03,
#     ser_conf
#     );


# frame = FRAME(
#     FRAME.FRAME_TYPE.MODULE_CONFIG,
#     FRAME.COMMAND_TYPE.MODULE_CONFIG.WRITE_CONFIG,
#     test.value())


# frame_data=FRAME(
#     FRAME.FRAME_TYPE.APPLICATION_DATA,
#     FRAME.COMMAND_TYPE.APPLICATION_DATA.SEND,
#     FRAME_APPLICATION_DATA(
#         0x0001,
#         FRAME_APPLICATION_DATA.WAIT_ACK.DISABLED,
#         0x03,
#         FRAME_APPLICATION_DATA.ROUTE_DISCOVERY.DISABLED,
#         [0xaa, 0xaa, 0xaa, 0xaa, 0xaa]).value())

# print(ser_conf.value())
# print(test.value().hex())


# for b in frame_data.value():
#     print("{:02x}".format(b), end = " ")

# print(frame.value().hex())

# print("{0:b}".format(test.value()))
