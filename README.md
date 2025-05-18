# DoS/DDoS Simulation & Detection Tools

A pair of Python scripts for simulating and detecting TCP SYN flood attacks on Windows using Scapy and Npcap.

## Contents

- `dos_ddos_simulator.py`  
  Simulate DoS and DDoS attacks by sending forged TCP SYN floods.

- `ddos_detector_windows.py`  
  Detect SYN flood attacks by sniffing SYN packets on a specified interface.

- `requirements.txt`  
  Lists Python dependencies.

- **Optional** test helpers:  
  - `test_sniffer.py` — verify packet capture.  
  - `test_syn_sender.py` — send manual SYNs for quick detector testing.

- `.gitignore`  
  Recommended to ignore `__pycache__/`, virtualenv folders, etc.

---

## Prerequisites

- **Python 3.6+**  
- **Npcap** installed with WinPcap API compatibility, you can download from [Npcap Download](https://npcap.com/#download)
- **Administrator** privileges to run raw sockets and sniff packets  

---

## Installation

1. Clone or download the repository.  
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Npcap is installed in WinPcap-compatible mode.

## Usage

1. Run the Detector (Laptop A)
   ```
    cd path\to\project
    python ddos_detector_windows.py \
      --iface "Wi-Fi" \
      --window 10       # sliding window in seconds \
      --threshold 200   # SYNs per IP per window to trigger alert
    ```
    Example output:
    ```
    [+] Listening on Wi-Fi, window=10.0s, threshold=200 SYNs
    [!] ALERT: 13.45.78.102 sent 230 SYNs in last 10.0s
    ```
2. Run the Simulator (Laptop B)
   ```
   cd path\to\project
   python dos_ddos_simulator.py \
    --target 123.456.78.900 \
    --mode ddos      # 'dos' or 'ddos' \
    --rate 100       # packets per second per thread \
    --threads 4      # threads for ddos mode
   ```
  Example output:
  ```
  [+] Starting DDoS on 123.456.78.900:80 with 4 threads × 100 pps each
  ```
  Replace 123.456.78.900 with your detector machine’s IP.

## Optional Testing Scripts
- ```test_sniffer.py```
  Verifies that packet capture works on your interface.
  ```python test_sniffer.py```

- ```test_syn_sender.py```
  Sends a burst of TCP SYNs for quick detector validation.
  ```python test_syn_sender.py```

## Contributing

Contributions are welcome! Please:

1. Fork the repo

2. Create a feature branch: git checkout -b feat/YourFeature

3. Commit your changes: `git commit -m "Add feature"

4. Push branch: git push origin feat/YourFeature

5. Open a pull request

## License
This project is licensed under the MIT License. See [LICENSE](https://github.com/PraveenkrishnaPK/DOS-DDOS-Tools/blob/main/LICENSE) for details.





