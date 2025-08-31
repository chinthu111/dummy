# DDIL Scenario 3 — **Bandwidth-Constrained Link**

This scenario simulates a **narrowband tactical link** (e.g., HF/SATCOM) by restricting the available bandwidth between assets.  
We measure how inter-asset communication and **Performance Efficiency** KPIs are impacted when the link has **very limited throughput** but remains functional.

---

## Goal

Validate system behavior under **low-bandwidth conditions**:
- TCP sessions stay up but throughput drops sharply.
- Comss-GW queues may **grow** if messages exceed available bandwidth.
- GraphQL pub/sub messages may be **delayed** due to slower transfer.

---

## Preconditions

- Three asset networks (10.10.2/24, 10.10.1/24, 10.10.3/24) attached to `ddil-router`.
- Comss-GW IPs: A1=`10.10.2.11`, A2=`10.10.1.10`, A3=`10.10.3.10`.

Find the router interface for the asset link to limit (example shows A2):
```bash
docker exec -it ddil-router sh -lc 'ip -o -4 addr show | grep 10\.10'
# Identify the iface that has 10.10.1.254/24 -> use that as ETH_A2 (e.g., eth1)


# Limit Asset-2 link to 128 kbps with a small burst buffer and latency tolerance
docker exec -it ddil-router sh -lc '
tc qdisc add dev eth1 root tbf rate 128kbit burst 16kbit latency 300ms'


# Show applied bandwidth settings
docker exec -it ddil-router tc qdisc show dev eth1



**Expected System Behavior
Functional

A2 ⇄ (A1,A3): TCP connections stay established, but throughput is capped.

GraphQL cross-asset: messages and subscriptions still work but respond slower.

Within A2: local communication is unaffected.**


Restore (end of test)
docker exec -it ddil-router tc qdisc del dev eth1 root


Verify restoration

docker exec -it ddil-router tc qdisc show dev eth1   # should show "noqueue"
docker exec -it ddil-router ping -c3 10.10.1.10     # RTT and speed back to normal
