What the scenario means
This scenario emulates a satellite or long-range link between two assets, where:

The connection is stable, but

The latency is very high (due to long distances),

The bandwidth is limited, and

There is light packet loss.

This type of environment is typical in remote operations where assets communicate over satellite or HF radios.

🔹 How to simulate it
Apply the following network impairments on the DDIL router between Asset 1 and Asset 2:

bash
Copy
Edit
# On the DDIL router (eth interfaces linked to Asset 1 and 2):
tc qdisc add dev eth1 root netem delay 1500ms 300ms distribution normal rate 128kbit loss 3%
tc qdisc add dev eth2 root netem delay 1500ms 300ms distribution normal rate 128kbit loss 3%
delay: 1500ms RTT (simulates satellite delay)

jitter: ±300ms

rate: 128kbps bandwidth cap

loss: 3% random packet loss

🔹 What you're testing (Mapped to ISD Characteristics)
ISD Characteristic Category	What We're Testing in This Scenario
Time Behavior	- Write-to-Listen Latency (End-to-End)
- Resolver Execution Time
- Sync Latency (eventual and strong)
Resource Utilization	- CPU usage during constrained sync
- Memory usage when buffering messages
Sync Behavior	- Stability of COMS Gateway in slow environments
- Zenoh queue behavior
Capacity / Performance	- Throughput impact under bandwidth limits
- GraphQL request timeout behavior

🔹 What’s the network setup
All assets are running as Docker containers on a single Ubuntu VM

A dedicated DDIL router container connects Asset 1 and Asset 2 via isolated Docker bridge networks

Only the link between Asset 1 and Asset 2 is degraded

markdown
Copy
Edit
+-------------------------------------------------------------+
|                      Ubuntu VM (local)                      |
|                                                             |
|   [Asset 1] ----> eth1 --+                         +--> eth2 ---- [Asset 2]  |
|                          |                         |                       |
|                        [DDIL Router] (tc netem) <--+                       |
|                                                             |
+-------------------------------------------------------------+
🔹 How to measure outcomes
KPI / Metric	Measurement Method
Write-to-Listen Latency	Time between a write on Asset 1 and a listen event on Asset 2
Sync Completion Time	Time it takes to sync state from Asset 1 to Asset 2
GraphQL Read/Write Latency (P95)	GraphQL server logs / metrics or Prometheus exporters
Resource Usage (CPU/Memory)	Docker stats or OTEL collector metrics
Throughput (Write/Listen Mbit/s)	Log data volume transferred over time
Message Drop or Timeout Rate	Application logs, Zenoh debug mode, GraphQL error responses
Queue Size / Buffering Behavior	Zenoh logs (if enabled) or custom instrumentation

🧩 Step-by-Step Procedure (Local Testbed)
Start all assets (6 groups of containers) using Docker Compose

On the DDIL router container, identify interfaces for Asset 1 and Asset 2

Apply the tc netem rules only to those interfaces

Generate regular write operations from Asset 1 to a topic

Have Asset 2 listening on the same topic

Monitor sync time, listen latency, and system resource usage

Log key events from:

graphql-server (request/response latency)

comsgateway (sync delays, retries)

zenohd (message flow, retries if available)

Docker stats / OTEL metrics (CPU, memory, throughput)

