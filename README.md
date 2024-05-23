# vpn-gcn

## 1. Download and install Wireshark
* While installing wireshark, CHECK the following option: Install Npcap in WinPcap API-compatible mode
## 2. Set Wireshark to environment variable
* In start menu search environment
* Edit the system environment variables > Environment Variables
* In user variable double-click Path
* Click New
* Paste the Wireshark installation path: (C:\Program Files\Wireshark)
* Click Ok > OK

## 3. Download the datasets
### 3A. (ISCX-VPN-NonVPN-2016)

http://205.174.165.80/CICDataset/ISCX-VPN-NonVPN-2016/Dataset/PCAPs/

* Download following files:
```
1. NonVPN-PCAPs-01.zip
2. NonVPN-PCAPs-02.zip
3. NonVPN-PCAPs-03.zip
4. VPN-PCAPS-01.zip
5. VPN-PCAPS-02.zip
```
### 3B. (VNAT-VPN)
https://archive.ll.mit.edu/datasets/vnat/VNAT_release_1.zip
* Download following files:
```
1. VNAT_release_1.zip
```

## 4. Prepare the datasets
### 4A. (ISCX-VPN-NonVPN-2016)

* Extract the following files in folder datasets/ISCX
```
NonVPN-PCAPs-01.zip
NonVPN-PCAPs-02.zip
NonVPN-PCAPs-03.zip
VPN-PCAPS-01.zip
VPN-PCAPS-02.zip
```

* Finally the dataset structure should look like:
```
-datasets
 - ISCX
  - aim_chat_3a.pcap
  - aim_chat_3b.pcap
	...
  - youtubeHTML5_1.pcap
  - vpn_aim_chat1a.pcap
  - vpn_aim_chat1b.pcap
	...
  - vpn_youtube_A.pcap
```
### 4B. (VNAT-VPN)
* Extract the following files in folder datasets/VNAT-VPN
```
VNAT_release_1.zip
```

## 5. Create conda environment and install packages
* Open miniconda and run following commands one-by-one:
```
create conda -n vpn-gcn python=3.11
conda activate vpn-gcn
pip install matplotlib, scapy, tqdm, pandas, numpy
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install torch_geometric
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.3.0+cu118.html
```

## 6. Convert pcapng files to pcap and split sessions
* Download splitcap utility
   https://www.netresec.com/?page=SplitCap
* Place SplitCap.exe file in .\vpn-gcn\scripts\
* Open project folder in VSCode
* Select python interpreter as "vpn-gcn"
* Run the script split_sessions.py

## 7. Process packets

* Run the script process_data.py
* This script will perform following tasks:
```
Read each sessions pcap file and extract first 10 packets.
For each packet, it
  Removes the Ethernet header.
  Masks source and destination IPs.
  Pads the UDP packets with zeros.
  Convert each packet to byte format (0-255 values), if any packet is less than 1500 it pads with zeros.
  Normalize each byte value into the range of (0.0 - 1.0).
  Generates CSV file with each row representing a packet.
```

## 8. Generate graphs
* Run the script generate_graphs.py

## 9. Train the model
* Run the script train.py
