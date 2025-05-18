from scapy.all import sniff, conf

def show(pkt):
    print(pkt.summary())

if __name__ == "__main__":
    print(f"[+] Sniffing on {conf.iface} (default) or specify with --iface below")
    sniff(iface="Wi-Fi", store=False, prn=show, count=20, timeout=15)
    print("[+] Done.")
