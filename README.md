# DDIL Scenario 4 — **Intermittent Connectivity (Flapping Link)**

This scenario simulates **unstable or flapping network links** by periodically **disconnecting and restoring** a specific asset link (e.g., **Asset-2 / 10.10.1.0/24**).  
We measure how inter-asset communication and **Performance Efficiency** KPIs are impacted when the connection repeatedly drops and recovers.

---

## Goal

Validate system behavior under **unstable network conditions**:
- TCP sessions disconnect and reconnect frequently.
- Comss-GW retries multiple times; queues may grow during outages.
- GraphQL pub/sub subscriptions drop and re-establish repeatedly.

---

## Preconditions

- Three asset networks (10.10.2/24, 10.10.1/24, 10.10.3/24) attached to `ddil-router`.
- Comss-GW IPs: A1=`10.10.2.11`, A2=`10.10.1.10`, A3=`10.10.3.10`.

Find the router interface for the asset link to flap (example shows A2):
```bash
docker exec -it ddil-router sh -lc 'ip -o -4 addr show | grep 10\.10'
# Identify the iface that has 10.10.1.254/24 -> use that as ETH_A2 (e.g., eth1)


# Simulate 10s down / 20s up for 3 cycles on Asset-2 link
docker exec -it ddil-router sh -lc '
IF=eth1
for i in 1 2 3; do
  echo "Cycle $i: Disconnecting $IF for 10s..."
  iptables -I FORWARD -i $IF -j DROP
  iptables -I FORWARD -o $IF -j DROP
  sleep 10

  echo "Cycle $i: Restoring $IF for 20s..."
  iptables -D FORWARD -i $IF -j DROP
  iptables -D FORWARD -o $IF -j DROP
  sleep 20
done'


Expected System Behavior
Functional

A2 ⇄ (A1,A3): TCP connections drop during down periods and reconnect after restoration.

GraphQL cross-asset: subscriptions disconnect during downtime and resubscribe automatically if configured.

Within A2: local communication remains normal.

**Success Criteria

Asset-2 link flaps according to timing (10s down / 20s up).

During downtime:

TCP sessions disconnect.

GraphQL subscriptions drop.

Comss-GW queues messages if buffering is enabled.

During uptime:

TCP sessions recover automatically.

GraphQL subscriptions reconnect.

Cross-asset communication resumes.

Upon completion, system returns to stable state.**


docker exec -it ddil-router sh -lc '
iptables -D FORWARD -i eth1 -j DROP || true
iptables -D FORWARD -o eth1 -j DROP || true'

docker exec -it ddil-router ping -c3 10.10.1.10    # consistent RTT again
docker logs --tail=50 comms-gw2                    # verify reconnect success
