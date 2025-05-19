import os
from scapy.all import rdpcap, IP, TCP, UDP, ICMP
from collections import defaultdict, Counter
from multiprocessing import Pool, cpu_count

# Parámetros para detección de anomalías
CONNECTION_THRESHOLD = 100
SUSPICIOUS_PORTS = {6667, 31337, 12345}


def format_bytes(size_bytes):
    """Convierte bytes a una cadena legible en MB o GB."""
    if size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / (1024**2):.2f} MB"
    else:
        return f"{size_bytes / (1024**3):.2f} GB"


def analyze_pcap(args):
    file_path, output_dir = args
    report_lines = []
    print(f"[+] Analizando: {file_path}")
    ip_counter = defaultdict(int)
    port_counter = defaultdict(int)
    protocol_counter = Counter()
    connection_set = set()
    ip_connection_counter = defaultdict(int)
    anomalies = []

    total_packets = 0
    total_bytes = 0

    try:
        packets = rdpcap(file_path)
    except Exception as e:
        print(f"[!] Error leyendo {file_path}: {e}")
        return

    for pkt in packets:
        total_packets += 1
        total_bytes += len(pkt)

        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            ip_counter[src_ip] += 1
            ip_counter[dst_ip] += 1
            ip_connection_counter[src_ip] += 1
            ip_connection_counter[dst_ip] += 1

        if TCP in pkt or UDP in pkt:
            sport = pkt.sport
            dport = pkt.dport
            port_counter[sport] += 1
            port_counter[dport] += 1
            connection_set.add((pkt[IP].src, sport, pkt[IP].dst, dport))

        if TCP in pkt:
            protocol_counter["TCP"] += 1
        elif UDP in pkt:
            protocol_counter["UDP"] += 1
        elif ICMP in pkt:
            protocol_counter["ICMP"] += 1
        else:
            protocol_counter["Otros"] += 1

    for ip, count in ip_connection_counter.items():
        if count > CONNECTION_THRESHOLD:
            anomalies.append(f"  - IP sospechosa: {ip} con {count} conexiones")

    for port in port_counter:
        if port in SUSPICIOUS_PORTS:
            anomalies.append(f"  - Puerto sospechoso usado: {port}")

    report_lines.append(f"REPORTE PARA: {os.path.basename(file_path)}\n")
    report_lines.append(f"Total de paquetes: {total_packets}")
    report_lines.append(f"Tráfico total: {format_bytes(total_bytes)}")
    report_lines.append(f"Conexiones únicas (IP:puerto): {len(connection_set)}")
    report_lines.append("\nProtocolos detectados:")
    for proto, count in protocol_counter.items():
        report_lines.append(f"  {proto}: {count}")

    report_lines.append("\nTráfico por IP (top 10):")
    for ip, count in sorted(ip_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        report_lines.append(f"  {ip}: {count} paquetes")

    report_lines.append("\nPuertos utilizados (top 10):")
    for port, count in sorted(port_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        report_lines.append(f"  {port}: {count} veces")

    if anomalies:
        report_lines.append("\nAnomalías detectadas:")
        report_lines.extend(anomalies)
    else:
        report_lines.append("\nNo se encontraron anomalías.")

    os.makedirs(output_dir, exist_ok=True)
    report_filename = os.path.basename(file_path) + "_report.txt"
    report_path = os.path.join(output_dir, report_filename)

    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))

    print(f"  >> Reporte generado en: {report_path}")


def analyze_directory_parallel(directory):
    output_dir = os.path.join(directory, "reportes")
    pcap_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".pcap")
    ]

    if not pcap_files:
        print("No se encontraron archivos .pcap en el directorio.")
        return

    print(f"[i] Analizando {len(pcap_files)} archivos usando {cpu_count()} núcleos...")

    # Empaquetar argumentos
    tasks = [(file_path, output_dir) for file_path in pcap_files]

    with Pool(processes=cpu_count()) as pool:
        pool.map(analyze_pcap, tasks)


if __name__ == "__main__":
    directory = input("Introduce la ruta del directorio que contiene archivos .pcap: ").strip()

    if not os.path.isdir(directory):
        print("❌ La ruta proporcionada no es un directorio válido.")
    else:
        analyze_directory_parallel(directory)
