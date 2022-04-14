






# DLR_QUIT            = ['quit',[]]
# DLR_CHANGE_SADDR    = ['chsaddr',['{:x}']]
# DLR_CHANGE_PANID    = ['chpanid',['{:x}']]
# DLR_CHANGE_CHANNEL  = ['chchann',['{:d}']]
# DLR_MODULE_VERSION  = ['modver',[]]

DLRMessageType = {
    'user': str,
    'timestamp': int,
    'message': str
}


class DeLoRa:

    DLR_PREFIX = '\\'


    def __init__(self):
        self.DLR_COM_LIST = {
            # 'help': [],
            'quit'      :[self.quit],
            'chsaddr'   :[],
            'chpanid'   :[],
            'chchannel' :[],
            'modver'    :[]
        }
        
        pass

    def send_query(self, query:str):

        if query.startswith(self.DLR_PREFIX):
            query = query[1:]
            if query in self.DLR_COM_LIST:
                return self.DLR_COM_LIST[query]
            else:
                return None
        pass

    def quit(self):
        pass


