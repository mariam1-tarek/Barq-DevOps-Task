# Troubleshooting journal

Keep chronological entries. Copy this block for each meaningful investigation.

## Issue 1: Upstream Connection Refused on app-02 / 13-9-2026 / 5:07 PM

* Symptom: NGINX fails to route traffic to the second backend instance, returning HTTP 502/503 response errors.
* Hypothesis: The app-02 instance is down or not listening on port 8080 .
* Command or test: grep -c "Connection refused" logs/error.log .
* Actual output: Found 59 connection failure events targeting http://172.23.0.12:8080 .
* Failed attempt and what changed your thinking:  None at this stage. Initial static log confirmed that app-02 was unreachable.
* Root cause: Will check container status in Part 2.
* Fix: will Add app-01 and app-02 to docker-compose.yml under frontend\_net.
* Retest evidence: Will test after Docker setup using validate.sh.
* Related commit: Baseline log analysis commit. 
* Remaining uncertainty: Need to review NGINX config and Flask code in Part 2.

## Issue 2: Misconfiguration at docker-compose at(App-host, instance id, path of postgre, tmpfs, nginx port)  / 13-9-2026 / 6:00 PM

* Symptom: Used wrong local host, both app instances reported the identity app-01, Postgre path must be to data not backup , and PostgreSQL data was stored in volatile memory, and NGINX was mapping to an incorrect internal port.
* Hypothesis: "APP_HOST" was restricted to "127.0.0.1", preventing container-to-container communication. "app-02" environment variable was incorrectly set to app-01, and NGINX target port was set to 81 instead of 80 , postgres-data to be at "/var/lib/postgresql/data" ,tmpfs usage.
* Command or test: cat docker-compose.yml
* Actual output:APP_HOST: "127.0.0.1", INSTANCE_ID: "app-01" , postgres-data:/var/lib/postgresql/backup , tmpfs and NGINX port mapped to 81.
* Failed attempt and what changed your thinking: None. Static configuration inspection confirmed all five mismatches
* Root cause: Flask app bound to local loopback inside containers instead of "0.0.0.0", duplicate "INSTANCE_ID" variable, postgre to wrong path, use tmpfs and NGINX mapped to wrong port.
* Fix: Changed APP_HOST to "0.0.0.0" in "docker-compose.yml", updated "app-02" INSTANCE_ID to "app-02", and corrected NGINX internal port mapping to 80 , changed postgres-data:/var/lib/postgresql/Backup to postgres-data:/var/lib/postgresql/data , remove tmpfs.
* Retest evidence: Verified updated configuration parameters in "docker-compose.yml".
* Related commit: Updated "docker-compose.yml" 
* Remaining uncertainty: need to perform Database and cache ports

## Issue 3: Invalid Database and Cache Ports  / 13-9-2026 / 6:45 PM

* Symptom: App services failed to reach PostgreSQL and Redis services.
* Hypothesis: Incorrect connection string ports in "app.env"
* Command or test: "cat config/app.env"
* Actual output: "DATABASE_URL" used port 5433, "REDIS_URL" used port 6380
* Failed attempt and what changed your thinking: None. File inspection clearly exposed port mismatches
* Root cause: Wrong internal container ports in env 
* Fix: Corrected connection ports to 5432 for Postgres and 6379 for Redis
* Retest evidence: onfiguration files updated and verified
* Related commit: Updated "config/app.env"
* Remaining uncertainty: Will confirm runtime data and connectivity during Docker startup.

Do not fabricate a failed attempt just to fill the template. Record actual attempts.

