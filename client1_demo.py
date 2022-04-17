import serial.tools.list_ports
import time

import YL800N

# TODO: Generate random short address from timestamp


# Print all available ports
port_list = list(serial.tools.list_ports.comports())


for i in range(len(port_list)):
    print(str(i) + " : " + str(port_list[i]))


port_choice = int(input("Enter the number of the port you want to use: "))
selected_port = port_list[port_choice]
module = YL800N.YL800N(selected_port.device)
module.open_communication()

# module_ver = module.feed_com(YL800N.COM_AT_VERSION)
# print(module_ver)


module.feed_com(YL800N.COM_AT_RESET)
module.feed_com(YL800N.COM_SWITCH_TO_AT) # Entering AT mode

saddr_choice = int(input("Enter the short address you want to use (1-65534): "))
module.feed_com(YL800N.COM_AT_SADDR, [saddr_choice])

# channel_choice = int(input("Enter the channel you want to use (0-32): "))
# module.feed_com(YL800N.COM_AT_CHANNEL, [channel_choice])
# module.feed_com(YL800N.COM_AT_ROLE, [YL800N.ROLE_SLAVE])


module.feed_com(YL800N.COM_AT_USERMODE, [YL800N.USERMODE_TRANSPARENT])


while True:
    user_msg = input("> ")
    # Convert message to hex
    user_msg = user_msg.encode()
    message_hex = ''.join(format(x, '02x') for x in user_msg)

    module.feed_com(YL800N.COM_SWITCH_TO_AT)
    module.feed_com(YL800N.COM_AT_SEND, [0xFFFF, message_hex])
    module.feed_com(YL800N.COM_AT_USERMODE, [YL800N.USERMODE_TRANSPARENT])



    


# module.close_com()

