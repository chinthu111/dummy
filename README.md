
`sh
docker exec -it ddil-router sh -lc '
A1_IF=$(ip -o -4 addr show | awk "/10\.10\.2\./ {print \$2; exit}");
A2_IF=$(ip -o -4 addr show | awk "/10\.10\.1\./ {print \$2; exit}");
A3_IF=$(ip -o -4 addr show | awk "/10\.10\.3\./ {print \$2; exit}");
echo "A1:$A1_IF  A2:$A2_IF  A3:$A3_IF"'
`

`
docker exec -it ddil-router sh -lc '
iptables -I FORWARD -i $A2_IF -j DROP
iptables -I FORWARD -o $A2_IF -j DROP'
docker exec -it ddil-router ping -c2 10.10.1.10
`
