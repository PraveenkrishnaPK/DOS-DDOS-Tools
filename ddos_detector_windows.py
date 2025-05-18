#!/usr/bin/env python3
"""
ddos_detector_windows.py

Detect TCP SYN‐flood attacks by counting SYN packets per source IP in a sliding window.

Usage (Windows Admin):
  python ddos_detector_windows.py --iface "Wi-Fi" --window 10 --threshold 200
  python ddos_detector_windows.py --list
"""
import argparse
import time
from collections import defaultdict, deque
from scapy.all import sniff, TCP, IP, conf

class SlidingWindowCounter:
    def __init__(self, window_size: float):
        self.window_size = window_size
        self.data = defaultdict(deque)

    def add(self, src_ip: str, timestamp: float):
        dq = self.data[src_ip]
        dq.append(timestamp)
        while dq and dq[0] < timestamp - self.window_size:
            dq.popleft()

    def count(self, src_ip: str) -> int:
        return len(self.data[src_ip])

def packet_callback(pkt, counter: SlidingWindowCounter, threshold: int):
    # look for SYN flag
    if IP in pkt and TCP in pkt and (pkt[TCP].flags & 0x02):
        src = pkt[IP].src
        now = time.time()
        counter.add(src, now)
        cnt = counter.count(src)
        if cnt > threshold:
            print(f"[!] ALERT: {src} sent {cnt} SYNs in last {counter.window_size:.1f}s")

def list_interfaces():
    print("Available NPF interfaces:")
    for iface in conf.ifaces.values():
        print(f"  {iface.name}\n    ↳ {iface.description}")

def main():
    parser = argparse.ArgumentParser(description="Windows DDoS SYN-flood detector")
    parser.add_argument("--list", action="store_true",
                        help="List available interfaces and exit")
    parser.add_argument("--iface", help="Interface name (e.g. 'Wi-Fi' or GUID')")
    parser.add_argument("--window", type=float, default=10.0,
                        help="Sliding window size in seconds (default: 10)")
    parser.add_argument("--threshold", type=int, default=200,
                        help="Alert threshold: SYNs per IP per window (default: 200)")
    args = parser.parse_args()

    if args.list:
        list_interfaces()
        return

    if not args.iface:
        parser.error("Please specify --iface or use --list to see options")

    counter = SlidingWindowCounter(args.window)
    print(f"[+] Listening on {args.iface}, window={args.window:.1f}s, threshold={args.threshold} SYNs")
    sniff(
        iface=args.iface,
        store=False,
        prn=lambda pkt: packet_callback(pkt, counter, args.threshold),
        filter="tcp[tcpflags] & tcp-syn != 0"
    )

if __name__ == "__main__":
    main()
