import os
import sys
import foxesscloud.openapi as f

def main():
    api_key = os.getenv("FOX_API_KEY")
    device_sn = os.getenv("FOX_DEVICE_SN", "60HD103058XM117")

    if not api_key:
        print("ERROR: FOX_API_KEY secret is missing")
        sys.exit(1)

    f.api_key = api_key
    f.device_sn = device_sn

    action = sys.argv[1] if len(sys.argv) > 1 else "off"
    print(f"=== Fox ESS Scheduler Control ===")
    print(f"Action requested : {action}")
    print(f"Inverter SN      : {device_sn}")

    # Load current schedule state
    try:
        schedule = f.get_schedule()
        print(f"Current scheduler enable flag: {schedule.get('enable') if schedule else 'unknown'}")
    except Exception as e:
        print(f"Warning while reading schedule: {e}")

    if action.lower() in ["off", "false", "0"]:
        print("→ Disabling Mode Scheduler (Self-use mode)...")
        try:
            result = f.set_schedule(enable=0)
            print(f"Disable result: {result}")
        except Exception as e:
            print(f"Error disabling scheduler: {e}")
            sys.exit(1)

    elif action.lower() in ["on", "true", "1"]:
        print("→ Enabling Mode Scheduler...")
        try:
            schedule = f.get_schedule()
            periods = schedule.get('periods') if schedule else None

            if periods:
                result = f.set_schedule(periods=periods, enable=1)
            else:
                # Fallback: full day SelfUse
                period = f.set_period(0, 24, "SelfUse", min_soc=10)
                result = f.set_schedule(periods=[period], enable=1)

            print(f"Enable result: {result}")
        except Exception as e:
            print(f"Error enabling scheduler: {e}")
            sys.exit(1)
    else:
        print("Unknown action. Use 'on'/'true' or 'off'/'false'")
        sys.exit(1)

    print("Done.")

if __name__ == "__main__":
    main()
