import usb_hid
from switchcontroller import SwitchController,Button
from time import sleep

sc = SwitchController(usb_hid.devices)
sc.reset_all()

while True:
    sc.push_button(Button.A, 0.1, 1)
