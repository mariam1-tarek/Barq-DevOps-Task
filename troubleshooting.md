# Troubleshooting journal

Keep chronological entries. Copy this block for each meaningful investigation.

## \## Issue 1: Upstream Connection Refused on app-02 / 13-9-2026 / 5:07 PM

* Symptom: NGINX fails to route traffic to the second backend instance, returning HTTP 502/503 response errors.
* Hypothesis: The app-02 instance is down or not listening on port 8080 .
* Command or test: `grep -c "Connection refused" logs/error.log` .
* Actual output: Found 59 connection failure events targeting http://172.23.0.12:8080 .
* Failed attempt and what changed your thinking:  None at this stage. Initial static log confirmed that app-02 was unreachable.
* Root cause: Will check container status in Part 2.
* Fix: will Add app-01 and app-02 to docker-compose.yml under frontend\_net.
* Retest evidence: Will test after Docker setup using validate.sh.
* Related commit: Baseline log analysis commit. 
* Remaining uncertainty: Need to review NGINX config and Flask code in Part 2.

Do not fabricate a failed attempt just to fill the template. Record actual attempts.

