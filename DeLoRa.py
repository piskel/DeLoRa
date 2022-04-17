import time

import YL800N


DLRMessageType = {
    'user': str,
    'timestamp': int,
    'message': str
}


class DeLoRa:

    DLR_PREFIX = '\\'


    def __init__(self, com_port, username):
        self.DLR_COM_LIST = {
            # 'help': [],
            'quit'      :[self.quit],
            'chsaddr'   :[],
            'chpanid'   :[],
            'chchannel' :[],
            'modver'    :[],
            'infos'     :[]
        }
        
        self.com_port = com_port
        self.module = YL800N.YL800N(com_port)
        self.module.open_communication()
        
        self.username = username
        self.saddr = 0
        self.panid = 0
        self.channel = 0




    def send_query(self, query:str):

        if query.startswith(self.DLR_PREFIX):
            query = query[1:]
            if query in self.DLR_COM_LIST:
                return self.DLR_COM_LIST[query]()
            else:
                return None
        else:
            message: DLRMessageType = {
                'user': self.username,
                'timestamp': int(time.time()),
                'message': query
            }

            # We send the message and directly switch back to transparent mode
            self.module.feed_com(YL800N.COM_SWITCH_TO_AT)
            self.module.feed_com(YL800N.COM_AT_SEND, [0xFFFF, message])
            self.module.feed_com(YL800N.COM_AT_USERMODE, [YL800N.USERMODE_TRANSPARENT])

            return message




    def get_new_messages(self):
        if not self.module.is_input_buffer_empty():
            return self.module.read_com()
        else:
            return None


    def quit(self):
        self.module.close_communication()


    
    # def chsaddr(self):


        

    





