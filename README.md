DDIL Scenario 1 — Disconnected Asset

This scenario intentionally isolates one asset network (e.g., Asset-2 / 10.10.1.0/24) from the others by dropping traffic on the DDIL router. We measure how inter-asset communication and Performance Efficiency KPIs are impacted while services inside each asset continue to run.

Goal

Validate system behavior when one asset is fully partitioned:

Comss-GW↔Comss-GW TCP sessions across the cut must fail.

Cross-asset GraphQL pub/sub must drop.

Same-asset communication stays normal.


Preconditions

Three asset networks (10.10.2/24, 10.10.1/24, 10.10.3/24) attached to ddil-router.

Comss-GW IPs: A1=10.10.2.11, A2=10.10.1.10, A3=10.10.3.10.

Apply (isolate Asset-2)


# Block inter-asset transit
docker exec -it ddil-router sh -lc '
iptables -I FORWARD -i eth1 -j DROP
iptables -I FORWARD -o eth1 -j DROP'

# Also block traffic to/from the router itself on that link
docker exec -it ddil-router sh -lc '
iptables -I INPUT  -i eth1 -j DROP
iptables -I OUTPUT -o eth1 -j DROP'


Expected System Behavior
Functional

A2 ⇄ (A1,A3): all new TCP connects fail; existing sessions die on keepalive/timeout.

GraphQL cross-asset: subscriptions and requests time out / disconnect.

Within A2: all same-asset communication is unaffected.




Performance Efficiency (impacted items)
ISD KPI area	Impact while isolated
Time behavior	
Initialization time (cold/hot)	If an asset starts while isolated and waits on cross-asset deps, startup may block until configured timeouts/backoff windows. Otherwise unchanged.
Nominal Read ops/s (req/resp)	Cross-asset reads involving A2 → 0 ops/s (fail/timeout). Intra-asset reads unaffected.
Nominal Write ops/s	Cross-asset writes to/from A2 → 0 ops/s. Intra-asset writes unaffected.
Read latency (overall / resolver / QoS / DB / networking)	Cross-asset “latency” manifests as timeouts (report as the timeout ceiling, e.g., 5s). Stddev low (mostly timeouts). Local latency unchanged.
Write latency (overall / resolver / QoS / DB / networking)	Same as read: timeouts for cross-asset paths; local unchanged.
Write/Listen end-to-end latency	Across the partition: no delivery (∞). Within same asset: unchanged.
Synchronization latency (eventual)	Unbounded growth for the isolated asset; state diverges until link heals.
Synchronization latency (strong)	Any strong/2-phase operations that require cross-asset coordination should fail fast.
Resource utilization	
Read/Write/Listen throughput (Mbit/s)	To/from A2 across the router: 0 Mbit/s delivered. (iptables DROP counters reflect attempted bytes.)
CPU usage	Comss-GW/clients may increase due to retries; if exponential backoff, stabilizes at a lower CPU.
Memory usage / Storage	If you buffer messages, queue depth grows (memory or disk). If not, messages are lost.
Capacity	Number of participants unchanged, but effective connectivity reduced; number of active remote subscriptions involving A2 drops to 0.
