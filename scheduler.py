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

    action = sys.argv[1] if len(sys.argv) > 1 else "off"
    print(f"Executing GitHub Action -> Action: {action}")

    # Explicitly bind your H3 Smart Inverter serial number
    device_sn = "60HD103058XM117"
    print(f"Target Inverter SN: {device_sn}")
    f.device_sn = device_sn

    # Initialize schedule session state (required before schedule/mode calls)
    try:
        f.get_schedule()
    except Exception as e:
        print(f"Note on get_schedule: {e}")

    if action == "off":
        print("Disabling Mode Scheduler and switching to SelfUse...")
        try:
            # Disable active schedule / Mode Scheduler lockout
            res_sched = f.set_schedule(enable=0)
            print(f"Disable schedule result: {res_sched}")
        except Exception as e:
            print(f"Disable schedule note: {e}")
            
        try:
            res_mode = f.set_work_mode('SelfUse')
            print(f"Set work mode result: {res_mode}")
        except Exception as e:
            print(f"Set work mode error: {e}")
    else:
        print("Switching work mode to FeedInFirst...")
        try:
            res_mode = f.set_work_mode('FeedInFirst')
            print(f"Set work mode result: {res_mode}")
        except Exception as e:
            print(f"Set work mode error: {e}")

if __name__ == "__main__":
    main()
