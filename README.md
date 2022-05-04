# DeLoRa - Decentralized LoRa messaging software

## Description
DeLoRa is a simple LoRa messaging program made for the YL-800N module from http://www.rf-module.cn/.


## Setup
The module should be connected to a computer through an USB to RS232 cable, either 3V3 or 5V. **WARNING : the cable connector may have to be rewired to match the pins of the module!**

The following cables have been used and **had to be rewired** in order to communicate properly with the LoRa module :
- TTL-232R-3V3 : https://ftdichip.com/products/ttl-232r-3v3/
- TTL-232R-5V : https://ftdichip.com/products/ttl-232r-5v/

Here are the pin connections for these cables.

| Cable pin colour | Connection to module |
| ---------------- | -------------------- |
| Black            | GND                  |
| Red              | VCC                  |
| Orange           | RXD                  |
| Yellow           | TXD                  |
| Green            | NC                   |
| Brown            | NC                   |

## Installation

Make sure to have Python 3.x installed on your machine, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

You can run the program with :

```bash
python main.py
```

## Usage
After starting the program, you should be met with the "Settings" tab. Set an username and make sure to use the COM port of the serial cable that is linked to your module. Then press apply.

You should now be able to send messages by going in the "Messages" tab.

At its current state, the program has to be configured in the settings tab before using it, otherwise it will crash.

## Warning !
In the YL800N class of the YL800N_HEX.py file, make sure that the `set_config()` method uses an appropriate TX power. Otherwise, depending on where you live, you might be infringing on local regulations.

## Miscellaneous

### YL800N_HEX.py

It should be noted that despite being still a work in progress, this file could already be used for other project using the YL-800N module.

### YL800N.py

This file was originally supposed to be used to communicate with the module in the way `YL800N_HEX.py` does, but by using AT commands. However, this mode proved to be quite unstable and the settings are not saved between resets. Even though this file is not actually used in the project anymore, it has been kept in the repo but might be deleted in the future.

### demo_sender.py / demo_receiver.py

Those file are useful to test that modules communicate properly, they are kept only for debugging purposes.

## Resources

- YL-800N manufacturer : http://www.rf-module.cn/
- Module page on DFRobot : https://www.dfrobot.com/product-1670.html
- Datasheet (chinese) : http://www.rf-module.cn/uploads/YL-800N.pdf