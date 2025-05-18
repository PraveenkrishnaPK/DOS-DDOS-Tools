# test_syn_sender.py
import time
from scapy.all import send, IP, TCP, conf

conf.iface = "Wi-Fi"  # make sure this matches your detector

def send_syns(src_ip, dst_ip, dst_port=80, count=20, delay=0.2):
    pkt = IP(src=src_ip, dst=dst_ip) / TCP(dport=dst_port, flags="S")
    for i in range(count):
        print(f"→ Sending SYN #{i+1} from {src_ip}")
        send(pkt, verbose=False)
        time.sleep(delay)

if __name__ == "__main__":
    TARGET = "192.168.29.112"  # your machine’s IP
    send_syns(src_ip="1.2.3.4", dst_ip=TARGET, count=20, delay=0.2)
