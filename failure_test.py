import subprocess
import urllib.request
import time
import sys

BASE_URL = "http://127.0.0.1:8080"

def check_availability(retries=5, delay=2):
    for _ in range(retries):
        try:
            req = urllib.request.Request(f"{BASE_URL}/instance")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(delay)
    return False

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print("Starting Failure and Recovery Test...\n")

    run_cmd("docker compose start app-01")
    time.sleep(2)

    print("Step 1: Stopping container 'app-01'...")
    if not run_cmd("docker compose stop app-01"):
        print("[FAIL] Failed to stop app-01")
        sys.exit(1)

    print("Step 2: Checking availability during failover...")
    if check_availability(retries=5, delay=2):
        print("[PASS] System remains available via app-02 during failure.")
    else:
        print("[FAIL] System unavailable after stopping app-01!")
        run_cmd("docker compose start app-01")
        sys.exit(1)

    print("Step 3: Restoring container 'app-01'...")
    if not run_cmd("docker compose start app-01"):
        print("[FAIL] Failed to start app-01")
        sys.exit(1)

    print("Step 4: Verifying recovered instance health...")
    if check_availability(retries=5, delay=2):
        print("[PASS] Recovered backend app-01 is serving requests successfully.")
    else:
        print("[FAIL] Failed to reach instance endpoint after recovery.")
        sys.exit(1)

    print("\n[PASS] Failure recovery test completed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()