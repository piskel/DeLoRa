import time
import tkinter as tk
from tkinter import ttk

import YL800N

DLRMessageType = {
    'username': str,
    'timestamp': int,
    'message': str,
}

class DeLoRa:
    
    def __init__(self, username):
        self.__com_port = None
        self.__username = username

        
        # Module configuration
        # self.__module.reset()
        # self.__module = YL800N.YL800N(com_port)
        # self.__module.open_communication()
        # self.__module.restore_defaults()
        # self.__module.role = YL800N.ROLE_SLAVE
    

    def set_com_port(self, com_port):
        self.__com_port = com_port

        if not self.__module.is_communication_open():
            self.__module.close_communication()
    
        self.__module = YL800N.YL800N(self.__com_port)
        self.__module.open_communication()
        self.__module.restore_defaults()
        self.__module.role = YL800N.ROLE_SLAVE

    # TODO: Allow to specify the sender
    def send_message(self, message:str):
        message = {
            'username': self.__username,
            'timestamp': int(time.time()),
            'message': message
        }

        self.__module.send_data(message)


    def check_messages(self):
        if not self.__module.is_input_buffer_empty():
            return self.__module.read_com()
    




    
