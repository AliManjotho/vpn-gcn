#This code removes the ethernet header of PCAP files
from scapy.all import *
import numpy as np
import pandas as pd
from scapy.compat import raw
from scapy.layers.inet import IP, UDP
from scapy.layers.inet6 import IPv6
from pathlib import Path
from tqdm import tqdm
from scapy.layers.l2 import Ether
import os



def preprocess(dataset_path, packets_per_session):

    files = list(Path(dataset_path).rglob('*.pcap'))
    pbar = tqdm(total=len(files), desc='Files Done: ')

    for file in files:
    
        if not Path(file.__str__()[:-4] + 'csv').is_file():

            pcap_reader = PcapReader(file.__str__())
            packet_list = pcap_reader.read_all(count=packets_per_session)

            z = []
            max = 1500
            if len(packet_list) > 2:
                for packet in packet_list:

                    # Remove ethernet header
                    #########################################################
                    if Ether in packet:
                        packet = packet[Ether].payload


                    # Mask IP
                    #########################################################
                    if IPv6 in packet:
                        packet[IPv6].dst = '0000::0:0'
                        packet[IPv6].src = '0000::0000:0000:0000:0000'

                    if IP in packet:
                        packet[IP].dst = '0.0.0.0'
                        packet[IP].src = '0.0.0.0'


                    # Pad UDP
                    #########################################################
                    if UDP in packet:
                        layer_after = packet[UDP].payload.copy()

                        pad = Padding()
                        pad.load = '\x00' * 12

                        layer_before = packet.copy()
                        layer_before[UDP].remove_payload()
                        packet = layer_before / raw(pad) / layer_after


                    # PCAP to CSV
                    #########################################################
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

            pbar.update(1)






if __name__=='__main__':
    packets_per_session = 10

    # Process ISCX dataset
    iscx_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\ISCX'
    preprocess(iscx_dataset_path, packets_per_session)

    # Process VNAT-VPN dataset
    # vnat_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\VNAT-VPN'
    # preprocess(vnat_dataset_path, packets_per_session)

    print('ALL DONE!!!!!')