from scapy.all import *
from scapy.utils import PcapWriter
from scapy.layers.l2 import Ether
from pathlib import Path
import os

dataset_path = 'D:/SH/TrafficClassification/dataset/ISCX/'
splitcap_path = '"D:/SH/TrafficClassification/code-gcn/PCAP processing/SplitCap.exe"'


command_1 = 'cd "' + dataset_path + 'NonVPN/"'
command_2 = splitcap_path + ' -r ' + dataset_path + 'NonVPN/ -recursive -s session'
command_3 = 'cd "' + dataset_path + 'VPN/"'
command_4 = splitcap_path + ' -r ' + dataset_path + 'VPN/ -recursive -s session'

# First run the following two lines and comment below two lines
# os.system(command_1)
# os.system(command_2)


# Second uncomment below two line and comment above two lines and run
os.system(command_3)
os.system(command_4)
