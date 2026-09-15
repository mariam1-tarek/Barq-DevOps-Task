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
* Hypothesis: "APP\_HOST" was restricted to "127.0.0.1", preventing container-to-container communication. "app-02" environment variable was incorrectly set to app-01, and NGINX target port was set to 81 instead of 80 , postgres-data to be at "/var/lib/postgresql/data" ,tmpfs usage.
* Command or test: cat docker-compose.yml
* Actual output:APP\_HOST: "127.0.0.1", INSTANCE\_ID: "app-01" , postgres-data:/var/lib/postgresql/backup , tmpfs and NGINX port mapped to 81.
* Failed attempt and what changed your thinking: None. Static configuration inspection confirmed all five mismatches
* Root cause: Flask app bound to local loopback inside containers instead of "0.0.0.0", duplicate "INSTANCE\_ID" variable, postgre to wrong path, use tmpfs and NGINX mapped to wrong port.
* Fix: Changed APP\_HOST to "0.0.0.0" in "docker-compose.yml", updated "app-02" INSTANCE\_ID to "app-02", and corrected NGINX internal port mapping to 80 , changed postgres-data:/var/lib/postgresql/Backup to postgres-data:/var/lib/postgresql/data , remove tmpfs.
* Retest evidence: Verified updated configuration parameters in "docker-compose.yml".
* Related commit: Updated "docker-compose.yml"
* Remaining uncertainty: need to perform Database and cache ports

## Issue 3: Invalid Database and Cache Ports  / 13-9-2026 / 6:45 PM

* Symptom: App services failed to reach PostgreSQL and Redis services.
* Hypothesis: Incorrect connection string ports in "app.env"
* Command or test: "cat config/app.env"
* Actual output: "DATABASE\_URL" used port 5433, "REDIS\_URL" used port 6380
* Failed attempt and what changed your thinking: None. File inspection clearly exposed port mismatches
* Root cause: Wrong internal container ports in env
* Fix: Corrected connection ports to 5432 for Postgres and 6379 for Redis
* Retest evidence: configuration files updated and verified
* Related commit: Updated "config/app.env"
* Remaining uncertainty: Will confirm runtime data and connectivity during Docker startup.



## Issue 4 NGINX Configuration Port Mismatch  / 14-9-2026 / 1:00 PM

* Symptom: NGINX failed to route traffic to Flask application backends correctly.
* Hypothesis: Internal mapping port inside nginx.conf did not match application port.
* Command or test: "cat nginx/nginx.conf ","curl -i http://127.0.0.1:8080/ "
* Actual output: 502 Bad Gateway
* Failed attempt and what changed your thinking:  Checked container logs, and found that forward requests to port 81 instead of 8080.
* Root cause: Mismatch between NGINX upstream and Flask application port.
* Fix: upstream port changed at nginx/nginx.conf to target port 8080.
* Retest evidence: "curl -i \[http://127.0.0.1:8080/]" returned HTTP/1.1 200 OK
* Related commit: Updated nginx/nginx.conf
* Remaining uncertainty: None



## Issue 5  PostgreSQL Credentials and Readiness Endpoint Mismatch / 14-9-2026 / 1:30 PM

* Symptom: Flask application failed database initialization and health checks failed.
* Hypothesis: PostgreSQL password in docker-compose.yml differed from app config, and healthcheck tested unhealthy endpoints
* Command or test: "docker compose logs app-01"
* Actual output:  Database connection authentication error, and healthcheck container marked as unhealthy
* Failed attempt and what changed your thinking:  Tried starting containers without updating healthcheck, causing app services to crash repeatedly on startup
* Root cause: Incorrect POSTGRES\_PASSWORD environment variable and using /healthz endpoint instead of /ready
* Fix: POSTGRES\_PASSWORD with BarqLabOnly\_7qN2vK8d and updated  healthcheck to /ready.
* Retest evidence: curl -i \[http://127.0.0.1:8080/ready] returned 200 OK
* Related commit: Updated docker-compose.yml
* Remaining uncertainty: None





## Issue 6 Remove Public Ports from PostgreSQL \& Redis and Network Isolation / 14-9-2026 / 2:30 PM

* Symptom: Internal backend database and cache were accessible from host interfaces , Need to enforce network isolation to prevent backend services from external internet
* Hypothesis: (PostgreSQL, Redis, Flask apps) have external access , network setup allows internal containers unrestricted external network egress.
* Command or test: " docker compose ps " , "docker-compose.yml"
* Actual output:  Ports 5432, 6379, and 8080 were publicly to external interfaces , no internal isolation to network
* Failed attempt and what changed your thinking:
* Root cause: non isolated network
* Fix: frontend and backend networks in docker-compose.yml and remove backend from nginx , leave only 8080 to nginx
* Retest evidence: Verified via docker compose ps that only NGINX exposes port 127.0.0.1:8080 is 80.
* Related commit: Updated docker-compose.yml
* Remaining uncertainty: None





## Issue 7  Need to let restart unless-stopped and limit resources / 14-9-2026 / 4:30 PM

* Symptom: Containers failed to automatically restart after unexpected process crashes or system reboots.
* Hypothesis: Container restart policies
* Command or test: grep -i "restart" docker-compose.yml
* Actual output:  Found default restart: "no"
* Failed attempt and what changed your thinking: Tested crashing a container manually, but Docker did not attempt to restart it automatically
* Root cause:
* Fix: NGINX to restart: "unless-stopped" and across all 5 container(postgres, redis, app-01, app-02) and put limits at cpu and memory
* Retest evidence:
* Related commit: Updated docker-compose.yml
* Remaining uncertainty:





## Issue 8  / 15-9-2026 / 12:30 PM

* Symptom: when run python code of failure\_test.py it gives msg ( system unavailable after stopping app-01!)
* Hypothesis: tried to write code again with increase delay to give time to system up 
* Command or test: docker compose start app-01 , docker compose restart nginx , python failure\_test.py
* Actual output:  \[FAIL] System unavailable after stopping app-01!
* Failed attempt and what changed your thinking:  change failure\_test.py code and increase delay time 
* Root cause: at nginx/nginx.conf need to add max\_fail , fail\_timeout and upstream
* Fix: add max\_fails=1 fail\_timeout=2s at upstream app-01 and app-02 and proxy\_next\_upstream error timeout http\_500 http\_502 http\_503 http\_504;
* Retest evidence: python failure\_test.py output is successfully 
* Related commit: Updated nginx/nginx.conf
* Remaining uncertainty: None 

























Do not fabricate a failed attempt just to fill the template. Record actual attempts.

