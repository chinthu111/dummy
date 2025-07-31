These reflect overall performance, availability, and consistency of the ISD under DDIL conditions.

KPI Name	Description
End-to-End Write-to-Listen Latency   	Time from a write operation on one asset to listen reception on another.
Sync Latency (Eventual Consistency)	   Time to propagate a change to a single peer asset (after proximity discovery).
Sync Latency (Strong Consistency)	   Time to ensure all active assets receive the update and are in sync.
System Initialization Time (Cold/Hot)	  Time to fully start and reach operational state with or without preloaded data.
Nominal Read Ops/sec	   Avg number of read ops the system can handle per second.
Nominal Write Ops/sec   	Avg number of write ops per second.
Data Delivery Success Rate [%]	% o f successful listen deliveries over total expected deliveries.
System Availability    [%]	Uptime and responsiveness during DDIL simulation.
Recovery Time After Disconnect	Time for a participant to rejoin, sync, and resume operations after drop.
Participant Scaling Threshold	Max number of concurrent participants supported before performance degrades.



✅ Low-Level KPIs (Component-Level Metrics)
These track performance inside GraphQL, Zenoh, sync logic, and infrastructure under constrained conditions.

KPI Name	Description
GraphQL Read Latency [Mean/P95/P99]	Time from read request to response (includes resolver and DB).
GraphQL Write Latency [Mean/P95/P99]	Time from write mutation to completion/ack.
Resolver Execution Duration	Time GraphQL resolvers spend processing logic.
QoS Resource Allocation Latency	Time to allocate topics/resources internally.
Local DB Latency	Time to fetch/update in-memory state.
Zenoh Routing Latency	Time for a message to travel from publisher to listener via Zenoh.
Zenoh Queue Depth	Number of messages queued when bandwidth is limited.
Packet Retransmission Rate	% of messages that were retried due to loss or delay.
CPU Usage [%]	CPU usage per service under typical and DDIL stress load.
Memory Usage [MB]	RAM usage of each ISD container or component.
Read Throughput [Mbit/s]	Network rate during read-intensive operations.
Write Throughput [Mbit/s]	Network rate during write-intensive operations.
Listen Throughput [Mbit/s]	Network rate for streamed or event-driven listens.
Data Dropped Due to Timeout	% of operations that failed because of link delay or queue overflow.
Duplicate Message Rate	% of duplicate messages received (e.g., due to reconnections).
Storage Usage [Bytes]	Total size of cached/synced data during test.
Latency Variation Across Participants	Deviation in performance among multiple connected assets.












 KPI Classification Matrix
Metric	Level	Type
Write-to-Listen Latency	High-Level	Time Behavior
Resolver Execution Duration	Low-Level	Internal Timing
CPU Usage	Low-Level	Resource Util.
Sync Latency (Strong)	High-Level	Consistency/Sync
Zenoh Queue Depth	Low-Level	System Buffering
Read Throughput	Low-Level	Network Load
Recovery Time	High-Level	Availability
