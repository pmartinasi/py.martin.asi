import os
from scapy.all import rdpcap, IP, TCP, UDP
from collections import defaultdict

# Umbrales configurables (solo se usan estos dos ahora)
CONNECTION_THRESHOLD = 100  # número de conexiones por IP
SUSPICIOUS_PORTS = {6667, 31337, 12345}  # ejemplos de puertos sospechosos

def analyze_pcap(file_path):
    print(f"\nAnalizando: {file_path}")
    ip_connection_counter = defaultdict(int)
    port_usage_counter = defaultdict(int)
    anomalies = []

    try:
        packets = rdpcap(file_path)
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return

    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            ip_connection_counter[src_ip] += 1
            ip_connection_counter[dst_ip] += 1

        if TCP in pkt or UDP in pkt:
            sport = pkt.sport
            dport = pkt.dport
            port_usage_counter[sport] += 1
            port_usage_counter[dport] += 1

    # Detectar anomalías (sin chequear número total de paquetes)
    for ip, count in ip_connection_counter.items():
        if count > CONNECTION_THRESHOLD:
            anomalies.append(f"  - IP sospechosa: {ip} con {count} conexiones")

    for port in port_usage_counter:
        if port in SUSPICIOUS_PORTS:
            anomalies.append(f"  - Puerto sospechoso usado: {port}")

    if anomalies:
        print(f"  >> Anomalías encontradas en {file_path}:")
        for a in anomalies:
            print(a)
    else:
        print("  >> No se encontraron anomalías.")

def analyze_directory(directory):
    pcap_files = [f for f in os.listdir(directory) if f.endswith(".pcap")]
    if not pcap_files:
        print("No se encontraron archivos .pcap en el directorio.")
        return

    for filename in pcap_files:
        file_path = os.path.join(directory, filename)
        analyze_pcap(file_path)

if __name__ == "__main__":
    directory = input("Introduce la ruta del directorio que contiene archivos .pcap: ").strip()

    if not os.path.isdir(directory):
        print("❌ La ruta proporcionada no es un directorio válido.")
    else:
        analyze_directory(directory)
