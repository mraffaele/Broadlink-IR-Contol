# Broadlink IR Remote Control

I use this with the Broadlink RM4 Mini (IR Blaster) to control various devices in my office, such as lights, fans etc.

The script allows you to toggle these devices on and off using their respective IR codes.

# Prerequisites

- Python 3.x
- [broadlink library](https://github.com/mjg59/python-broadlink) (install using `pip install broadlink`).
- A Broadlink RM4 Mini device set up and connected to your network.

# Config

## Device IP Address

If you know the IP address of your Broadlink device, you can set it directly in the `DEVICE_IP` variable in `toggle.py`.

If not, running any action (e.g. `python toggle.py learn`) will trigger a discovery process to find the device on the network. This may take a few seconds, and once found, it will print the IP address of the device.

> Device discovered slowly. IP detected: IP_ADDRESS

Grab this IP and update it in the `DEVICE_IP` variable for faster access in the future.

# Learning IR Codes

1. Run this command to enter learning mode: `python toggle.py learn`

2. Press the button on your remote that you want to learn. The script will capture the IR code and print it in the console.

3. Copy the printed IR code and update the corresponding entry in the `DEVICES_IRS` dictionary in `toggle.py` with the new code. E.g.

```
DEVICES_IRS = {
    "LIGHT": "IR_CODE_FOR_LIGHT",
}
```

4. Do this for each device you want to control.

# Toggling Devices

To toggle a device on or off, run the script with the device name as an argument. For example, to toggle the light:

`python toggle.py light`

This will send the learned IR code for the light to the Broadlink device, which will then transmit it to the target device..

You can queue multiple toggles like so: `python toggle.py light fan tv`. It will trigger them sequentially with a short delay in between.
