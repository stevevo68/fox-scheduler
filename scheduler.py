import os
import sys
import foxesscloud.foxesscloud as f

def main():
    api_key = os.getenv("FOX_API_KEY")
    username = os.getenv("FOX_USERNAME")
    password = os.getenv("FOX_PASSWORD")

    if not api_key:
        print("ERROR: FOX_API_KEY environment variable not set.")
        sys.exit(1)

    # Configure authentication
    f.api_key = api_key
    if username:
        f.username = username
    if password:
        f.password = password

    action = sys.argv[1] if len(sys.argv) > 1 else "on"
    print(f"Executing GitHub Action -> Action: {action}")

    # Fetch devices (returns a dictionary keyed by device serial number)
    devices = f.get_device()
    if not devices:
        print("ERROR: No Fox ESS devices found.")
        sys.exit(1)

    # Extract your inverter's serial number and assign it explicitly
    device_sn = list(devices.keys())[0] if isinstance(devices, dict) else devices[0].get('deviceSN')
    print(f"Target Device SN: {device_sn}")
    f.device_sn = device_sn

    if action == "off":
        print("Switching inverter work mode to Self-Use...")
        result = f.set_work_mode('SelfUse')
        print(f"Set work mode result: {result}")
    else:
        print("Switching inverter work mode to FeedInFirst...")
        result = f.set_work_mode('FeedInFirst')
        print(f"Set work mode result: {result}")

if __name__ == "__main__":
    main()
