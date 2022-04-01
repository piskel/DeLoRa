import serial.tools.list_ports
from soupsieve import select

import YL800N



# Print all available ports
port_list = list(serial.tools.list_ports.comports())


for i in range(len(port_list)):
    print(str(i) + " : " + str(port_list[i]))


port_choice = int(input("Enter the number of the port you want to use: "))
selected_port = port_list[port_choice]
print(selected_port.device)


module = YL800N.YL800N(YL800N.ROLE_SLAVE, 0x01, selected_port.device)
module.open_com()
module.configure()
# print(module.get_version())
module.send_message("ffff", "pouet")
