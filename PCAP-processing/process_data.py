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
import sys

def getfilesize(file):
    size = os.path.getsize(file)
    return str(round(size/(1024*1024), 4)) + ' MB'

def preprocess(dataset_path, packets_per_session):

    files = list(Path(dataset_path).rglob('*.pcap'))

    for file_index, file in enumerate(files):
    
        if not Path(file.__str__()[:-4] + 'csv').is_file():

            z = []
            max = 1500

            pcap_reader = PcapReader(file.__str__())
            packet_list = pcap_reader.read_all(count=packets_per_session)

            
            
            if len(packet_list) > 2:
                for packet_index, packet in enumerate(packet_list):

                    prompt = '===========================================================================================================================================================\n'
                    prompt += 'Files processed: {}/{}\n'.format(file_index,len(files))
                    prompt += 'Currently processing: {} ({})\n'.format(file.__str__(), getfilesize(file.__str__()))
                    prompt += 'Packets processed: {}/{}\n'.format(packet_index,len(packet_list))
                    prompt += '==========================================================================================================================================================='
                    print(prompt)

                    prompt_lines = 5
                    for _ in range(0,prompt_lines):
                        sys.stdout.write("\x1b[1A\x1b[2K")


                    # Remove ethernet header

                    if Ether in packet:
                        packet = packet[Ether].payload


                    # Mask IP

                    if IPv6 in packet:
                        packet[IPv6].dst = '0000::0:0'
                        packet[IPv6].src = '0000::0000:0000:0000:0000'

                    if IP in packet:
                        packet[IP].dst = '0.0.0.0'
                        packet[IP].src = '0.0.0.0'


                    # Pad UDP

                    if UDP in packet:
                        layer_after = packet[UDP].payload.copy()

                        pad = Padding()
                        pad.load = '\x00' * 12

                        layer_before = packet.copy()
                        layer_before[UDP].remove_payload()
                        packet = layer_before / raw(pad) / layer_after


                    # PCAP to CSV

                    t = np.frombuffer(raw(packet), dtype=np.uint8)[0: max] / 255
                    if len(t) <= max:
                        pad_width = max - len(t)
                        t = np.pad(t, pad_width=(0, pad_width), constant_values=0)
                        z.append(t)

                    df = pd.DataFrame(z)
                    df.to_csv(file.__str__()[:-4] + 'csv', index=False, header=False)
                    z.clear()

            pcap_reader.close()

            if os.path.isfile(file.__str__()):
                os.remove(file.__str__())






if __name__=='__main__':

    packets_per_session = 10
    dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\dataset\ISCX'
    preprocess(dataset_path, packets_per_session)
    print('ALL DONE!!!!!')