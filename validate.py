import urllib.request
import urllib.error
import socket
import time
import sys

BASE_URL = "http://127.0.0.1:8080"
ENDPOINTS = ["/", "/health", "/ready", "/counter", "/records", "/instance"]
ISOLATED_PORTS = [5432, 6379]
MAX_RETRIES = 5
RETRY_DELAY = 3

def test_endpoint(endpoint):
    url = BASE_URL + endpoint
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return True
    except Exception:
        pass
    return False

def test_port_closed(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', port))
        return result != 0

def main():
    print("Starting Validation Checks...\n")
    all_passed = False

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"--- Attempt {attempt}/{MAX_RETRIES} ---")
        success = True

        for ep in ENDPOINTS:
            if test_endpoint(ep):
                print(f"[PASS] Endpoint {ep} is reachable.")
            else:
                print(f"[FAIL] Endpoint {ep} failed.")
                success = False

        for port in ISOLATED_PORTS:
            if test_port_closed(port):
                print(f"[PASS] Port {port} is properly isolated.")
            else:
                print(f"[FAIL] Port {port} is exposed to host!")
                success = False

        if success:
            all_passed = True
            print("\n[PASS] All validation checks passed!")
            break
        else:
            print("Some checks failed. Retrying...\n")
            time.sleep(RETRY_DELAY)

    if not all_passed:
        print("\n[FAIL] Validation failed after maximum retries.")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
