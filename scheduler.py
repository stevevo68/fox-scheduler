import os
import sys
import foxesscloud.openapi as f

f.api_key = os.environ.get("FOX_API_KEY")
f.device_sn = "60HD103058XM117"


def main():
  try:
    print("Connecting to Fox ESS Cloud...")
    f.get_device()
    f.get_schedule()

    # Read action from command-line argument passed by GitHub Actions
    if len(sys.argv) > 1:
      action = sys.argv[1].lower()
    else:
      action = os.environ.get("ACTION_TYPE", "off").lower()

    print(f"Executing action: {action}")

    if action == "off":
      print(
          "Disabling Mode Scheduler and switching to Self-Use mode for"
          " overnight..."
      )
      # Pass an empty list [] as the first argument to clear and disable schedules
      res_sched = f.set_schedule([], enable=0)
      print("Schedule Disable API Result:", res_sched)

      # Explicitly set work mode to Self-Use so the app updates instantly
      res_mode = f.set_work_mode("SelfUse")
      print("Work Mode API Result:", res_mode)

    elif action == "on":
      print("Enabling Mode Scheduler...")
      res = f.set_schedule(enable=1)
      print("Schedule Enable API Result:", res)
    else:
      print(f"Unknown action specified: {action}")

  except Exception as e:
    print(f"Error executing command: {str(e)}")
    sys.exit(1)


if __name__ == "__main__":
  main()
