 Recovery After Full Blackout
🔹 What the scenario means
This scenario simulates a complete asset-level outage (e.g., due to power loss, software crash, or network failure) where the asset is:

Completely offline for an extended period (e.g., 5–10 minutes),

Then rejoins the network, reconnects with other assets, and must catch up on missed state and messages.

This reflects field scenarios like:

Temporary asset failure in harsh environments,

A rebooted node after mission redeployment.

🔹 How to simulate it
Stop all containers for one asset (e.g., Asset 6):

bash
Copy
Edit
docker stop asset6-graphql asset6-zenoh asset6-comsgateway asset6-influxdb
Wait for 5+ minutes (during which other assets continue normal operations).

Restart the containers:

bash
Copy
Edit
docker start asset6-graphql asset6-zenoh asset6-comsgateway asset6-influxdb
🔹 What you're testing (Mapped to ISD Characteristics)
ISD Characteristic Category	What We're Testing
Sync Behavior	- Replay of missed data from other assets
- COMS Gateway state re-init
Consistency & Recovery	- Data integrity after reconnection
- Eventual/strong sync resolution
Time Behavior	- Sync latency (post-blackout catch-up)
- Resolver recovery time
Resource Utilization	- CPU/Memory spike during catch-up
- Storage increase after syncing

🔹 What’s the network setup
All assets on a single Ubuntu VM with Docker.

Asset 6 is taken completely offline (containers stopped).

Other assets remain connected to DDIL router and continue operating normally.

markdown
Copy
Edit
+-------------------------------------------------------------------+
|                          Ubuntu VM (local)                        |
|                                                                   |
|  [Asset 1] --+                                                    |
|  [Asset 2] --+                                                    |
|     ...      +--> [DDIL Router] <---> [Asset 6] (offline 5 mins)  |
|                                                                   |
+-------------------------------------------------------------------+
