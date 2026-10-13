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

    f.api_key = api_key
    if username and password:
        f.username = username
        f.password = password

    action = sys.argv[1] if len(sys.argv) > 1 else "on"
    print(f"Executing GitHub Action -> Action: {action}")

    # Initialize device details
    devices = f.get_device()
    if not devices:
        print("ERROR: No Fox ESS devices found.")
        sys.exit(1)

    device_sn = devices[0].get('deviceSN') or devices[0].get('sn')
    print(f"Target Device SN: {device_sn}")

    # Sync schedule state
    f.get_schedule()

    if action == "off":
        print("Switching inverter work mode to Self-Use...")
        result = f.set_work_mode('SelfUse')
        print(f"Set work mode result: {result}")
    else:
        print("Applying Feed-in First mode...")
        result = f.set_work_mode('FeedInFirst')
        print(f"Set work mode result: {result}")

if __name__ == "__main__":
    main()
