# vpn-gcn
## 1. Download the dataset (ISCX-VPN-NonVPN-2016)

http://205.174.165.80/CICDataset/ISCX-VPN-NonVPN-2016/Dataset/PCAPs/

A. Download following files:
```
1. NonVPN-PCAPs-01.zip
2. NonVPN-PCAPs-02.zip
3. NonVPN-PCAPs-03.zip
4. VPN-PCAPS-01.zip
5. VPN-PCAPS-02.zip
```

## 2. Prepare dataset (ISCX-VPN-NonVPN-2016)

* Extract the following files in folder dataset/ISCX/NonVPN
- NonVPN-PCAPs-01.zip
- NonVPN-PCAPs-02.zip
- NonVPN-PCAPs-03.zip

* Extract the following files in folder dataset/ISCX/VPN
- VPN-PCAPS-01.zip
- VPN-PCAPS-02.zip

* Finally the dataset structure should look like:
```
-dataset
 - ISCX
   - NonVPN
     - aim_chat_3a.pcap
     - aim_chat_3b.pcap
	...
     - youtubeHTML5_1.pcap
  - VPN
    - vpn_aim_chat1a.pcap
    - vpn_aim_chat1b.pcap
	...
    - vpn_youtube_A.pcap
```
## 3. Convert pcapng files to pcap
* Run the script pcapng_to_pcap.py

## 4. Split Sessions

* Download splitcap utility
   https://www.netresec.com/?page=SplitCap
* Place SplitCap.exe file in .\code-gcn\PCAP processing\
* Right-Clik and edit SplitSessions.bat file.
* Set the dataset_path and splitcap_path accordingly and save.
* Double-click .\code-gcn\PCAP processing\SplitSessions.bat
* This will split pcap files in to sessions.

> [!NOTE]
> During Split, if the SplitCap.exe crashes then delete the following files from dataset:
> - ISCX/VPN/vpn_hangouts_audio1.pcap
> - ISCX/VPN/vpn_hangouts_audio2.pcap
