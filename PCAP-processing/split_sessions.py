#This code removes the ethernet header of PCAP files
from scapy.all import *
from scapy.compat import raw
from pathlib import Path
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
            print("File converted : ", old_file)

    print("No. of PCAPNG files converted to PCAP  : ", count)
    print('================================================================================')
    print('STEP 01: COMPLETED')
    print('')


def split_sessions_iscx(dataset_path, splitcap_path):
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

    print('================================================================================')
    print('STEP 02: COMPLETED')
    print('')


def split_sessions_vnat(dataset_path, splitcap_path):
    print("")
    print('STEP 02: STARTED (Splitting PCAP files into sessions)')
    print('================================================================================')

    splitcap_path = "\"" + splitcap_path + "\""

    split_dir = dataset_path + r'\Splitted'

    cmd1 = splitcap_path + " -r " +  dataset_path + " -o " + split_dir + " -recursive -s session"    
    cmd2 = "del /Q " + dataset_path + "\\*.pcap"
    cmd3 = "move /Y " + split_dir + "\\*.pcap " + dataset_path
    cmd4 = "rmdir /s /Q " + split_dir

    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)

    print('================================================================================')
    print('STEP 02: COMPLETED')
    print('')




if __name__=='__main__':
    splitcap_path= r'D:\SH\TrafficClassification\vpn-gcn\PCAP-processing\SplitCap.exe'
    
    # Split sessions for ISCX dataset
    iscx_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\ISCX'
    pcapng_to_pcap(iscx_dataset_path)
    split_sessions_iscx(iscx_dataset_path, splitcap_path)

    # Split sessions for VNAT-VPN dataset
    # vnat_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\VNAT-VPN'
    # pcapng_to_pcap(vnat_dataset_path)
    # split_sessions_vnat(vnat_dataset_path, splitcap_path)

    print('ALL DONE!!!!!')