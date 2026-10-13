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

    # Load inverter device details
    device_info = f.get_device()
    print(f"Connected to device successfully.")

    if action == "off":
        print("Switching inverter work mode to SelfUse...")
        result = f.set_work_mode('SelfUse')
        print(f"Set work mode result: {result}")
    else:
        print("Switching inverter work mode to FeedInFirst...")
        result = f.set_work_mode('FeedInFirst')
        print(f"Set work mode result: {result}")

if __name__ == "__main__":
    main()
