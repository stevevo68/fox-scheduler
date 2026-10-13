import os
import sys
import foxesscloud.openapi as f

# Initialize credentials and device SN
f.api_key = os.environ.get("FOX_API_KEY")
f.device_sn = "60HD103058XM117"


def main():
  try:
    print("Initializing connection to Fox ESS Cloud...")
    # Step 1: Fetch device info (mandatory for establishing session state)
    device = f.get_device()
    print(f"Device connected successfully: {device}")

    # Step 2: Fetch current schedule (mandatory for populating internal library flags)
    schedule_data = f.get_schedule()
    print("Schedule data retrieved successfully.")

    # Determine action from command-line argument passed by GitHub Actions
    if len(sys.argv) > 1:
      action = sys.argv[1].lower()
    else:
      action = os.environ.get("ACTION_TYPE", "off").lower()

    print(f"Executing action: {action}")

    if action == "off":
      print(
          "Disabling Mode Scheduler and forcing Self-Use mode for overnight..."
      )
      # Disable the schedule
      res_sched = f.set_schedule(enable=0)
      print("Schedule Disable API Result:", res_sched)

      # Explicitly set work mode to Self-Use so the app updates instantly
      res_mode = f.set_work_mode("SelfUse")
      print("Work Mode API Result:", res_mode)

    elif action == "on":
      print("Enabling Mode Scheduler (Resuming scheduled work modes)...")
      res = f.set_schedule(enable=1)
      print("Schedule Enable API Result:", res)
    else:
      print(f"Unknown action specified: {action}")

  except Exception as e:
    print(f"Error executing command: {str(e)}")
    sys.exit(1)


if __name__ == "__main__":
  main()
