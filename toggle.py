import sys
import broadlink
import binascii
import time
import threading

DEVICE_IP = "127.0.0.1"

DEVICES_IRS = {
    "device_1": "IR_CODE_FOR_DEVICE_1",
    "device_2": "IR_CODE_FOR_DEVICE_2",
}

ACTIONS = list(DEVICES_IRS.keys()) + ["learn"]

def connect_broadlink():
    try:
        device = broadlink.hello(DEVICE_IP)
        print("Device found by IP.")
    except:
        devices = broadlink.discover(timeout=3)
        if len(devices) > 0:
            device = devices[0]
            print("Device discovered slowly. IP detected: ", device.host)
        else:
            print("No devices found on the network.")
            sys.exit(1)
            return None


    device.auth()
    print("Authenticated.")
    return device

def validate_user_action():
    if len(sys.argv) < 2:
        print(f"Usage: python toggleDevice.py [{'|'.join(ACTIONS)}] ...")
        sys.exit(1)

    args = [a.lower() for a in sys.argv[1:]]

    if "learn" in args:
        if len(args) > 1:
            print("Warning: 'learn' ignored when combined with other actions")
            args = [a for a in args if a != "learn"]
        else:
            return ["learn"]

    invalid = [a for a in args if a not in ACTIONS]
    if invalid:
        print(f"Unknown action(s): {', '.join(invalid)}")
        sys.exit(1)

    return args

def toggle_device(controller, action):
    device_ir = DEVICES_IRS[action]
    print(f"Sending IR signal ({action})...")
    controller.send_data(binascii.unhexlify(device_ir))

def wait_for_enter(done_event):
    input()
    done_event.set()
    


def learning_mode(controller, timeout=10):
    stop_event = threading.Event()

    t = threading.Thread(target=wait_for_enter, args=(stop_event,), daemon=True)
    t.start()

    print(f"Learning mode: press remote button (auto-finish on signal or {timeout}s timeout)")
    controller.enter_learning()

    start = time.time()

    while time.time() - start < timeout:
        if stop_event.is_set():
            print("Cancelled by user (Enter pressed)")
            return

        try:
            data = controller.check_data()
            if data:
                print("Signal received:")
                print(data.hex())
                return
        except Exception:
            pass

        time.sleep(0.2)

    print("No signal captured within timeout")


def __main__():
    actions = validate_user_action()
    controller = connect_broadlink()

    if actions == ["learn"]:
        learning_mode(controller)
    else:
        for i, action in enumerate(actions):
            toggle_device(controller, action)
            if i < len(actions) - 1:
                time.sleep(0.1)
    sys.exit(0)

__main__()

