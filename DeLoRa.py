import time
import json
import random

from YL800N_HEX import *

DLRMessageType = {
    'username': str,
    'timestamp': int,
    'message': str,
}

class DeLoRa:
    
    def __init__(self, username, com_port):
        self.__username = username
        self.__com_port = com_port
        self.__module = YL800N(self.__com_port)

        # if not self.__module.is_communication_open():
        #     self.__module.close_communication()
    
        self.__module.open_communication()
        self.__module.set_config(
            channel=FRAME_MODULE_CONFIG.CHANNEL.CH432M,
            user_mode=FRAME_MODULE_CONFIG.USER_MODE.HEXADECIMAL,
            role=FRAME_MODULE_CONFIG.ROLE.SLAVE,
            network_flag=0x0000,
            node_flag=random.randint(0,0xFFFE))
    
    def stop(self):
        self.__module.close_communication()


    # TODO: Allow to specify the sender
    def send_message(self, message:str):
        message = {
            'username': self.__username,
            'timestamp': int(time.time()),
            'message': message
        }
        str_message = json.dumps(message, ensure_ascii=False)

        self.__module.send_string(0xFFFF,str_message)
        return str_message


    def check_messages(self):
        if not self.__module.is_input_buffer_empty():
            return self.__module.read_com()
    
    def is_input_buffer_empty(self):
        return self.__module.is_input_buffer_empty()
        
    def read_com(self):
        packet = self.__module.read_com()
        frame = FRAME.decoder(packet)
        print(frame)
        if frame is None or frame.payload is None:
            return None
        return frame.payload.payload


    
