#This code removes the ethernet header of PCAP files
from scapy.all import *
import glob
import numpy as np
import pandas as pd
from scapy.compat import raw
from scapy.layers.inet import IP, UDP
from scapy.layers.inet6 import IPv6
from pathlib import Path
from tqdm import tqdm
import concurrent.futures
from scapy.layers.l2 import Ether
import os

def pcapng_to_pcap(dataset_path):
    print("")
    print('STEP 01: STARTED (Converting PCAPNG files to PCAP)')
    print('================================================================================')

    files = list(Path(dataset_path).rglob('*.pcap*'))
    
    count = 0
    for file in files:
        old_file = file.resolve().__str__()
        new_file = old_file.replace("pcapng", "pcap")

        if old_file[-7:len(old_file)] == '.pcapng':
            command = "editcap -F libpcap -T ether " + old_file + " " + new_file
            os.system(command)
            os.remove(old_file)
            count = count + 1
            print("File converted : ", new_file)

    print("No. of PCAPNG files converted to PCAP  : ", count)
    print('================================================================================')
    print('STEP 01: COMPLETED')
    print('')


def split_sessions(dataset_path, splitcap_path):
    print("")
    print('STEP 02: STARTED (Splitting PCAP files into sessions)')
    print('================================================================================')


    corrupted_file1 = dataset_path + r'\VPN\vpn_hangouts_audio1.pcap'
    corrupted_file2 = dataset_path + r'\VPN\vpn_hangouts_audio2.pcap'
    
    if os.path.isfile(corrupted_file1):
        os.remove(corrupted_file1)
    if os.path.isfile(corrupted_file2):
        os.remove(corrupted_file2)


    splitcap_path = "\"" + splitcap_path + "\""

    nonvpn_split_dir = dataset_path + r'\NonVPN-Splitted'
    vpn_split_dir = dataset_path + r'\VPN-Splitted'
    nonvpn_dir = dataset_path + r'\NonVPN'
    vpn_dir = dataset_path + r'\VPN'

    cmd1 = splitcap_path + " -r " +  nonvpn_dir + " -o " + nonvpn_split_dir + " -recursive -s session"    
    cmd2 = splitcap_path + " -r " +  vpn_dir + " -o " + vpn_split_dir + " -recursive -s session"
    cmd3 = "rmdir /s /Q " + nonvpn_dir
    cmd4 = "rmdir /s /Q " + vpn_dir
    cmd5 = "move " + nonvpn_split_dir + " " + nonvpn_dir
    cmd6 = "move " + vpn_split_dir + " " + vpn_dir

    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)
    # print(cmd1)
    # print(cmd2)
    # print(cmd3)
    # print(cmd4)
    # print(cmd5)
    # print(cmd6)

    print('================================================================================')
    print('STEP 02: COMPLETED')
    print('')




if __name__=='__main__':

    dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\dataset\ISCX'
    splitcap_path= r'D:\SH\TrafficClassification\vpn-gcn\PCAP-processing\SplitCap.exe'
    
    pcapng_to_pcap(dataset_path)
    split_sessions(dataset_path, splitcap_path)

    print('ALL DONE!!!!!')