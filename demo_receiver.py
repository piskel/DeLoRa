from YL800N_HEX import *
import time


port_list = YL800N.get_com_port_list()

for i in range(len(port_list)):
    print(str(i) + " : " + str(port_list[i]))


port_choice = int(input("Enter the number of the port you want to use: "))
selected_port = port_list[port_choice]
module = YL800N(selected_port)
module.open_communication()

saddr_choice = int(input("Enter the short address you want to use (1-65534): "))


module.set_config(
    channel=FRAME_MODULE_CONFIG.CHANNEL.CH432M,
    user_mode=FRAME_MODULE_CONFIG.USER_MODE.HEXADECIMAL,
    role=FRAME_MODULE_CONFIG.ROLE.SLAVE,
    network_flag=0x0000,
    node_flag=saddr_choice)

while True:
    if not module.is_input_buffer_empty():
        print(module.read_com())
    time.sleep(0.1)

    

    