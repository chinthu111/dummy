DDIL Network Setup

This project sets up a simulated DDIL (Disconnected, Degraded, Intermittent, and Limited) network using Docker Compose.
It creates three isolated asset networks (Asset 1, Asset 2, Asset 3) that are interconnected via a DDIL router.

How the Setup Works

Three user-defined Docker networks are created:

Asset 1 → 10.10.2.0/24

Asset 2 → 10.10.1.0/24

Asset 3 → 10.10.3.0/24

Each asset has:

A Zenoh router for data exchange.

A Comss-GW node for communication.

Optional GraphQL and Dummy containers.

The DDIL router:

Connects all three networks.

Has IPs .254 on each subnet.

Enables IP forwarding (net.ipv4.ip_forward=1).

Allows inter-network routing via iptables -P FORWARD ACCEPT.

How to Deploy
# Start everything
docker compose up -d

# Stop everything
docker compose down

How to Verify the Setup
1. Check container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Networks}}"

2. Verify IP addressing
docker exec -it comms-gw1 ip a
docker exec -it comms-gw2 ip a
docker exec -it comms-gw3 ip a

3. Test routing between assets
# From Asset 1 → Asset 2 & Asset 3
docker exec -it comms-gw1 ping -c2 10.10.1.10
docker exec -it comms-gw1 ping -c2 10.10.3.10

# From Asset 2 → Asset 1 & Asset 3
docker exec -it comms-gw2 ping -c2 10.10.2.11
docker exec -it comms-gw2 ping -c2 10.10.3.10

# From Asset 3 → Asset 1 & Asset 2
docker exec -it comms-gw3 ping -c2 10.10.2.11
docker exec -it comms-gw3 ping -c2 10.10.1.10

4. Check router forwarding
docker exec -it ddil-router sysctl net.ipv4.ip_forward
docker exec -it ddil-router iptables -S FORWARD


Expected:

net.ipv4.ip_forward = 1
-P FORWARD ACCEPT

Key Points

All inter-network traffic flows through the DDIL router.

.254 is the gateway IP for each subnet.

Comss-GW containers add static routes pointing to the DDIL router.

Zenoh routers enable messaging between assets.

GraphQL and Dummy containers stay isolated within their own subnet.
