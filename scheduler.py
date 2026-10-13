import os
import sys
import foxesscloud.foxesscloud as f

def main():
    api_key = os.getenv("FOX_API_KEY")
    if not api_key:
        print("ERROR: FOX_API_KEY environment variable not set.")
        sys.exit(1)

    action = sys.argv[1] if len(sys.argv) > 1 else "on"
    print(f"Executing GitHub Action -> Action: {action}")

    # Initialize API key
    f.api_key = api_key
    
    # Get device list
    devices = f.get_device()
    if not devices:
        print("ERROR: No Fox ESS devices found for this API key.")
        sys.exit(1)
    
    device_sn = devices[0].get('deviceSN') or devices[0].get('sn')
    print(f"Target Device SN: {device_sn}")

    # Initialize library state
    f.get_schedule()

    if action == "off":
        print("Switching inverter work mode to Self-Use...")
        result = f.set_work_mode('SelfUse')
        print(f"Set work mode result: {result}")
    else:
        print("Applying schedule / work mode...")
        # Add your schedule logic here for 'on'
        result = f.set_work_mode('FeedInFirst') # or your preferred scheduler mode
        print(f"Set work mode result: {result}")

if __name__ == "__main__":
    main()
