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
module = YL800N.YL800N(selected_port)
module.open_communication()
module.role = YL800N.ROLE_SLAVE


module.reset()
saddr_choice = int(input("Enter the short address you want to use (1-65534): "))
module.saddr = saddr_choice



buffer = ""
new_buffer = ""
while True:
    # new_buffer += module.read_com()


    if not module.is_input_buffer_empty():
        print(module.read_com())
    
    time.sleep(0.1)


    


# module.close_com()

