import hashlib
import os
import sys
import time
import requests

API_KEY = os.environ.get("FOX_API_KEY")
DEVICE_SN = "60HD103058XM117"
BASE_URL = "https://www.foxesscloud.com"


def get_signature(path, token):
  """Generates the required signature headers for Fox ESS OpenAPI."""
  timestamp = str(int(time.time() * 1000))
  signature_str = f"{path}\r\n{token}\r\n{timestamp}"
  signature = hashlib.md5(signature_str.encode("utf-8")).hexdigest()

  return {
      "token": token,
      "timestamp": timestamp,
      "signature": signature,
      "lang": "en",
      "Content-Type": "application/json",
      # CRITICAL: Custom User-Agent prevents Fox ESS / Cloudflare from silently dropping POST requests
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      ),
  }


def set_mode_scheduler(enable: int):
  """Calls the Fox ESS Open API to enable (1) or disable (0) the Mode Scheduler."""
  path = "/op/v0/device/scheduler/enable"
  url = f"{BASE_URL}{path}"

  headers = get_signature(path, API_KEY)
  payload = {"sn": DEVICE_SN, "enable": enable}

  print(f"Sending request to {url} with enable={enable}...")
  response = requests.post(url, json=payload, headers=headers, timeout=15)

  print(f"HTTP Status Code: {response.status_code}")
  print(f"Raw Response Body: {response.text}")

  res_json = response.json()
  if res_json.get("errno") == 0:
    print("SUCCESS: Fox ESS Cloud accepted the schedule command!")
  else:
    print(f"FAILURE: Fox ESS returned error code: {res_json}")


def main():
  if not API_KEY:
    print("ERROR: FOX_API_KEY environment variable is missing!")
    sys.exit(1)

  # Read command line argument
  if len(sys.argv) > 1:
    action = sys.argv[1].lower()
  else:
    action = os.environ.get("ACTION_TYPE", "off").lower()

  print(f"Executing GitHub Action for device {DEVICE_SN} -> Action: {action}")

  if action == "off":
    print("Disabling Mode Scheduler...")
    set_mode_scheduler(0)
  elif action == "on":
    print("Enabling Mode Scheduler...")
    set_mode_scheduler(1)
  else:
    print(f"Unknown action: {action}")


if __name__ == "__main__":
  main()
