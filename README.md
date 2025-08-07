Low Latency + Intermittent Connectivity (Mobile Node Simulation)
🔹 What the scenario means
This scenario emulates a mobile asset (e.g., drone, vehicle, or field unit) that has a good quality connection when in range, but frequently disconnects and reconnects due to movement or unstable radio coverage.

Unlike high latency links, this connection is fast when active, but unreliable.

🔹 How to simulate it
Keep baseline latency low (e.g., 100ms), but simulate link loss periodically by disconnecting and reconnecting the asset from its network:

bash
Copy
Edit
# Simulate link loss for 30 seconds every few minutes
docker network disconnect net-asset3 asset3-comsgateway
sleep 30
docker network connect net-asset3 asset3-comsgateway
Optionally, you can use tc loss and delay before/after to simulate signal degradation:

bash
Copy
Edit
tc qdisc add dev ethX root netem delay 100ms loss 2%
🔹 What you're testing (Mapped to ISD Characteristics)
ISD Characteristic Category	What We're Testing
Time Behavior	- Reconnection latency
- Resume time for sync and listeners
Sync Behavior	- Sync consistency after disconnection
- State catch-up timing
Resource Utilization	- CPU/memory spikes during resync
System Availability	- Listen reliability after reconnect
- Application resilience

🔹 What’s the network setup
Asset 3 is running in a Docker container on Ubuntu VM

Asset 3 is intermittently disconnected from the DDIL router

COMS Gateway uses known IPs — sync must resume after reconnect

markdown
Copy
Edit
+-------------------------------------------------------------+
|                      Ubuntu VM (local)                      |
|                                                             |
| [Asset 3] <-- connect/disconnect --> [DDIL Router] <---> Other Assets |
|                                                             |
+-------------------------------------------------------------+
All other assets stay connected to the DDIL router

Only Asset 3’s network is manipulated to simulate mobility

🔹 How to measure outcomes
KPI / Metric	Measurement Method
Reconnection Time	Time from reconnect to operational sync (comsgateway logs)
Missed Message Recovery	# of messages sent during disconnect vs recovered after reconnect
Sync Catch-Up Duration	Time for Asset 3 to fully sync after rejoining
Duplicate Message Rate	Application logs (compare write/listen IDs)
System Stability	Any crashes, errors, or stuck listeners on reconnect
CPU/Memory Spikes	Docker stats, OTEL, or Prometheus monitoring
