import os
import foxesscloud.openapi as f

f.api_key = os.environ.get("FOX_API_KEY")
f.device_sn = "60HD103058XM117"


def main():
  try:
    f.get_device()
    f.get_schedule()

    action = os.environ.get("ACTION_TYPE", "off")

    if action == "off":
      print(
          "Disabling Mode Scheduler (Switching to Self-Use for 0% DoD"
          " overnight)..."
      )
      res = f.set_schedule(enable=0)
      print("API Result:", res)
    elif action == "on":
      print("Enabling Mode Scheduler (Resuming scheduled work modes)...")
      res = f.set_schedule(enable=1)
      print("API Result:", res)
  except Exception as e:
    print("Error executing command:", str(e))


if __name__ == "__main__":
  main()
