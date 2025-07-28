# dummy
dummy-python
1. What to Simulate in a DDIL Environment
For ISD testing, you should cover both network-level conditions and operational behaviors your system will face.

A. Network Impairments
These reflect what tactical, mobile, or satellite links experience:

Latency:

Fixed delays (200ms, 500ms, 1500ms).

Jitter (±50–500ms) to simulate unstable paths.

Bandwidth Limits:

Constrained (e.g., 64 kbps, 256 kbps, 1 Mbps).

Sudden fluctuations (e.g., 64 kbps → 512 kbps → 0).

Packet Loss:

Random (1–10%).

Burst loss (several packets dropped in a row).

Packet Duplication or Reordering:

Some links cause out-of-order delivery.

Corruption:

Occasional bit errors (forces retries).

Intermittent Connectivity:

Assets go offline for seconds/minutes (simulate mobility or range).

Rejoin events should be tested for recovery.

B. Proximity & Mobility
Nodes “discover” each other only when in range (simulate by toggling links).

Overlapping vs non-overlapping connectivity zones:

Some nodes can see each other, others can’t.

Changing topologies (mesh formation and teardown).

C. Load & Scaling
Vary number of topics and subscribers (e.g., 10 vs 500).

Test large payloads (video, large JSON) vs small updates (status pings).

Introduce publish bursts (e.g., 100 messages per second for 10 seconds).

2. KPIs to Measure for ISD
To validate your ISD, measure end-to-end performance, reliability, and resilience.

A. Data Delivery Metrics
Delivery Latency

Time from publisher send → subscriber receive.

Measure 50th/95th/99th percentile latency under various impairments.

Throughput / Goodput

How much data actually reaches subscribers (vs dropped)?

Measured in kbps per topic and per node.

Message Delivery Ratio

Delivered messages ÷ Sent messages (should be >99% unless you intentionally drop).

Message Order Integrity

Are events delivered in order, even after reconnects?

B. System Resilience & Behavior
Recovery Time After Disconnect

How quickly can a node resync after being offline?

Are missed messages replayed, or do subscribers just pick up from "now"?

Queueing/Buffering Behavior

Does the publisher buffer for slow links?

Measure queue sizes and dropped messages when bandwidth drops.

Interest Registration Success Rate

Can nodes reliably register interest (topics) under network stress?

Are subscriptions persistent across reconnects?

Protocol Robustness

Does GraphQL pub-sub (via WebSockets/MQTT/HTTP) reconnect gracefully?

Do retries cause duplicates or missed events?

C. Resource Impact
CPU/Memory Usage Under Stress

Does the ISD degrade gracefully, or crash when links get bad?

Especially when buffering or retrying.

Network Overhead

How much control traffic (heartbeats, discovery, retries) vs actual data?

High overhead can kill performance on low-bandwidth links.

3. Test Scenarios to Cover
For a comprehensive DDIL test, design test cases like:

High latency + low bandwidth (satellite-like).

Low latency + intermittent connectivity (mobile ad-hoc).

Burst packet loss during heavy traffic.

Multiple nodes coming in and out of range (mesh).

Slow subscriber (backpressure scenario).

Large number of topics with varying interest levels.

Recovery after full blackout (node offline 5 minutes).

