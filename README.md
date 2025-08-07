 Test Scenario 1: High Latency + Low Bandwidth (Satellite-Like Link)
🔹 What the scenario means:
Simulates communication over a satellite-like link with very high delay and low bandwidth, but stable connectivity.

🔹 How to simulate it:
Apply tc (traffic control) on the DDIL router interface connected to Asset 1 and Asset 2:

bash
Copy
Edit
tc qdisc add dev ethX root netem delay 1500ms 300ms rate 128kbit loss 3%
🔹 What you’re testing:
Can sync operate reliably with high latency and limited bandwidth?

Does GraphQL respond within acceptable time?

Are listen operations stable under slow conditions?

🔹 What’s the network setup:
Local Ubuntu VM running:

Asset 1 and Asset 2 (each as a group of Docker containers)

A central DDIL router container

Each asset connected via a dedicated Docker bridge network

All traffic between assets flows through the DDIL router

pgsql
Copy
Edit
Asset 1 <---> DDIL Router <---> Asset 2
(tc delay + bandwidth applied on both links)
🔹 How to measure outcomes:
End-to-end write-to-listen latency

GraphQL operation response time

Sync completion time (logs from comsgateway)

CPU and memory usage during constrained sync

Packet retransmissions (optional via logs or Wireshark)
