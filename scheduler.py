import os
import sys
import time
import foxesscloud.openapi as f   # important: use openapi

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

    # Load current schedule state (required by the library)
    try:
        schedule = f.get_schedule()
        print(f"Current scheduler enable flag: {schedule.get('enable') if schedule else 'unknown'}")
    except Exception as e:
        print(f"Warning while reading schedule: {e}")

    if action.lower() == "off":
        print("→ Disabling Mode Scheduler (this should put the inverter into Self-use)...")
        try:
            result = f.set_schedule(enable=0)   # This is the correct way
            print(f"Disable result: {result}")
        except Exception as e:
            print(f"Error disabling scheduler: {e}")
            sys.exit(1)

    elif action.lower() == "on":
        print("→ Enabling Mode Scheduler...")
        # You must supply at least one period when enabling.
        # Here we just re-enable whatever is already configured on the inverter.
        try:
            # First make sure we have the current periods
            schedule = f.get_schedule()
            periods = schedule.get('periods') if schedule else None

            if periods:
                result = f.set_schedule(periods=periods, enable=1)
            else:
                # Fallback – enable with a full-day SelfUse period
                period = f.set_period(0, 24, "SelfUse", min_soc=10)
                result = f.set_schedule(periods=[period], enable=1)

            print(f"Enable result: {result}")
        except Exception as e:
            print(f"Error enabling scheduler: {e}")
            sys.exit(1)
    else:
        print("Unknown action. Use 'on' or 'off'")
        sys.exit(1)

    print("Done.")

if __name__ == "__main__":
    main()
