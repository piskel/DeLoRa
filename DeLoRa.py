import time
import json
import random

from YL800N_HEX import YL800N, FRAME, FRAME_MODULE_CONFIG

DLRMessageType = {
    'username': str,
    'timestamp': int,
    'message': str,
}

class DeLoRa:
    """
    Class to handle the communication with the DeLoRa module.
    """
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
        """Stop the communication."""
        self.__module.close_communication()


    def send_message(self, message:str):
        """Send a message to the DeLoRa module."""
        # TODO: Allow to specify the sender
        message = {
            'username': self.__username,
            'timestamp': int(time.time()),
            'message': message
        }
        str_message = json.dumps(message, ensure_ascii=False)

        self.__module.send_string(0xFFFF,str_message)
        return str_message


    # def check_messages(self):
    #     """Check if there are messages in the input buffer and returns them if there are any."""
    #     if not self.__module.is_input_buffer_empty():
    #         return self.__module.read_com()

    # TODO: Handle messages at a higher level
    def is_input_buffer_empty(self):
        """Checks if there are any new messages in the input buffer."""
        return self.__module.is_input_buffer_empty()
       
    def read_com(self):
        """Reads a message from the input buffer."""
        packet = self.__module.read_com()
        frame = FRAME.decoder(packet)
        print(frame)
        if frame is None or frame.payload is None:
            return None
        return frame.payload.payload
