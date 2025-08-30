docker exec -it ddil-router sh -lc '
A1_IF=$(ip -o -4 addr show | awk "/10\.10\.2\./ {print \$2; exit}");
A2_IF=$(ip -o -4 addr show | awk "/10\.10\.1\./ {print \$2; exit}");
A3_IF=$(ip -o -4 addr show | awk "/10\.10\.3\./ {print \$2; exit}");
echo "A1:$A1_IF  A2:$A2_IF  A3:$A3_IF"'
