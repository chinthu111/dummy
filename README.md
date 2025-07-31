What is a DDIL Environment in Our ISD Context?

  A DDIL environment for your ISD is a degraded and constrained communication scenario where:

Assets (nodes) operate under:

High latency (e.g., 500–2000ms RTT)

Low bandwidth (e.g., 64–512 kbps)

Packet loss or jitter

Intermittent connectivity

Participants may sync eventually or strongly, depending on context.

All ISD modules (GraphQL, Zenoh, storage, apps) must remain functionally resilient and efficient.



These are the DDIL stress variables you’ll simulate across scenarios:

Parameter	Why It Matters
Latency [ms]	Affects request/response, sync delays
Jitter [ms]	Breaks protocol expectations, retries/resends
Bandwidth [kbps]	Limits throughput, stresses buffering
Packet Loss [%]	Tests retransmission, resiliency
Disconnection Duration [s]	Tests reconnect & sync correctness
Message Size [B]	Stresses compression & transport efficiency
Number of Participants	Tests scalability & system contention


ISD Behaviors to Monitor and Validate

Time Behavior
Initialization Time

Cold start (empty DB, full sync)

Hot start (preloaded data)

Operation Rates

Nominal read/write ops per second

End-to-End Latency

Read latency (request/response)

Write latency (request/ack)

Listen (write-to-receive propagation)

Resolver Timing

Resolver execution duration

QoS allocation latency

Local DB latency

Networking latency

📌 Synchronization
Sync Latency (Eventual Consistency)

Time from write → visible on another asset

Sync Latency (Strong Consistency)

Time from write → confirmed visible across all assets



High-Level KPIs

KPI Name	Description
End-to-End Write-to-Listen Latency	Time from write on one asset → listen received on another
Sync Completion Time	Time to sync state across 1 or all assets under delay
Read/Write Operation Rate	Nominal ops/sec (requests that succeed)
System Initialization Time	Cold vs hot start-up time under load
Availability Under DDIL	% time ISD responds to ops under constrained link

Low-Level KPIs
KPI Name	Description
GraphQL Read Latency [avg/p95/p99]	Request → Response
GraphQL Write Latency	Write → Ack
Resolver Execution Time	Query/mutation resolution duration
QoS Resource Allocation Time	Internal ISD latency for resource setup
Local DB Access Time	Cache or volatile store lookup latency
Zenoh Routing Delay	Publish → receive latency across Zenoh
Networking Delay (tc-level)	Confirmed latency/jitter at netem point
CPU Usage [%]	Under load, by service
Memory Usage [MB]	Peak + average usage
Listen Throughput [Mbit/s]	Write to listen data rate
Storage Usage	Total state size during steady state
Participant Scaling	# of active participants supported under DDIL
