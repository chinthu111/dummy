# DDIL Scenario 2 — **Degraded Link (High Latency + Jitter)**

This scenario simulates **SATCOM-like degraded conditions** on a specific asset link (e.g., **Asset-2 / 10.10.1.0/24**) by introducing **high latency, jitter, and optional packet loss** on the DDIL router.  
We measure how inter-asset communication and **Performance Efficiency** KPIs are affected when connectivity remains but performance degrades.

---

## Goal

Validate system behavior under poor network conditions:
- TCP sessions remain **connected** but slow.
- Comss-GW may **retry or timeout** depending on configuration.
- GraphQL pub/sub works but with **delays** and possible **out-of-order** updates.

---

## Preconditions

- Three asset networks (10.10.2/24, 10.10.1/24, 10.10.3/24) attached to `ddil-router`.
- Comss-GW IPs: A1=`10.10.2.11`, A2=`10.10.1.10`, A3=`10.10.3.10`.

Find the router interface for the asset link to degrade (example shows A2):
```bash
docker exec -it ddil-router sh -lc 'ip -o -4 addr show | grep 10\.10'
# Identify the iface that has 10.10.1.254/24 -> use that as ETH_A2 (e.g., eth1)


# Add 800ms average latency, ±200ms jitter, 5% packet loss
docker exec -it ddil-router sh -lc '
tc qdisc add dev eth1 root netem delay 800ms 200ms 25% loss 5%'

# Measure RTT from router — expect ~800ms or higher
docker exec -it ddil-router ping -c3 10.10.1.10



# Measure RTT from router to A2
docker exec -it ddil-router ping -c3 10.10.1.10

# Show applied netem settings
docker exec -it ddil-router tc qdisc show dev eth1


Success Criteria

A2 remains reachable but RTT increases significantly.

TCP connections stay alive, but throughput decreases.

GraphQL subscriptions work but with visible delays.

No service crashes or unexpected disconnects.

Upon restoring, system performance returns to normal.


docker exec -it ddil-router tc qdisc del dev eth1 root
docker exec -it ddil-router tc qdisc show dev eth1   # should show "noqueue"
docker exec -it ddil-router ping -c3 10.10.1.10     # RTT returns to normal
