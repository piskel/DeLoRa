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

If you don't have it already, install Python 3.X, then install the dependencies :

```bash
python -m pip install -r requirements.txt
```

And run the program with :

```bash
python main.py
```

## Usage
At its current state, the program has to be configured in the settings tab before using it, otherwise it will crash. Make sure to use the correct COM port. 

## Warning !
In the YL800N class of the YL800N_HEX.py file, make sure that the `set_config()` method uses an appropriate TX power. Otherwise, depending on where you live, you might be infringing on local regulations.


## Resources
- YL-800N manufacturer : http://www.rf-module.cn/
- Module page on DFRobot : https://www.dfrobot.com/product-1670.html
- Datasheet (chinese) : http://www.rf-module.cn/uploads/YL-800N.pdf