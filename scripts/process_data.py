import numpy as np
import os
import json
from scapy.all import *
from scapy.compat import raw
from scapy.layers.inet import IP, UDP
from scapy.layers.inet6 import IPv6
from pathlib import Path
from tqdm import tqdm
from scapy.layers.l2 import Ether
from utils import *

def myconverter(o):
    if isinstance(o, np.float32):
        return float(o)
    
def iscx_preprocess(dataset_path, packets_per_session):

    # Get list of all PCAP session file paths
    files = list(Path(dataset_path).rglob('*.pcap'))
    pbar = tqdm(total=len(files), desc='Files Done: ')

    for file_number, file in enumerate(files, start=1):

        pcap_reader = PcapReader(file.__str__())
        # Read first n packets of PCAP file, n=packets_per_session, we use n=10
        packet_list = pcap_reader.read_all(count=packets_per_session)

        features = []
        max = 1500
        json_str = {}

        # Session atleast has 3 packets
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


                # Convert PCAP to Byte format and normalize
                #########################################################
                t = np.frombuffer(raw(packet), dtype=np.uint8)[0: max] / 255
                if len(t) <= max:
                    pad_width = max - len(t)
                    t = np.pad(t, pad_width=(0, pad_width), constant_values=0)
                    features.append(t.tolist())

            # Save PCAP as JSON files
            #########################################################
            class_label = iscx_get_class_label(Path(file).name)
            one_hot_vector = iscx_get_one_hot(class_label)
            id = filenumber_to_id(file_number)
            json_str['id'] = id
            json_str['features'] = features
            json_str['edge_indices'] = num_packets_to_edge_indices(len(features))
            json_str['class'] = class_label
            json_str['class_vector'] = one_hot_vector  

            with open(dataset_path + '\\' + id + '.json', 'w') as f:
                f.write(json.dumps(json_str, default=myconverter))

            features.clear()

        pcap_reader.close()

        # Remove processed PCAP session file
        if os.path.isfile(file.__str__()):
            os.remove(file.__str__())

        # Update progress bar
        pbar.update(1)
        








def vnat_preprocess(dataset_path, packets_per_session):

    # Get list of all PCAP session file paths
    files = list(Path(dataset_path).rglob('*.pcap'))
    pbar = tqdm(total=len(files), desc='Files Done: ')

    for file_number, file in enumerate(files, start=1):

        pcap_reader = PcapReader(file.__str__())
        # Read first n packets of PCAP file, n=packets_per_session, we use n=10
        packet_list = pcap_reader.read_all(count=packets_per_session)

        features = []
        max = 1500
        json_data = {}

        # Session atleast has 3 packets
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


                # Convert PCAP to Byte format and normalize
                #########################################################
                t = np.frombuffer(raw(packet), dtype=np.uint8)[0: max] / 255
                if len(t) <= max:
                    pad_width = max - len(t)
                    t = np.pad(t, pad_width=(0, pad_width), constant_values=0)
                    features.append(t.tolist())

            # Save PCAP as JSON files
            #########################################################
            class_label = vnat_get_class_label(Path(file).name)
            one_hot_vector = vnat_get_one_hot(class_label)
            id = filenumber_to_id(file_number)
            json_data['id'] = id
            json_data['features'] = features
            json_data['edge_indices'] = num_packets_to_edge_indices(len(features))
            json_data['class'] = class_label
            json_data['class_vector'] = one_hot_vector
            json_str = json.dumps(json_data)
            
            with open(dataset_path + '\\' + id + '.json', 'w') as f:
                json.dump(json_str, f)

            features.clear()

        pcap_reader.close()

        # Remove processed PCAP session file
        if os.path.isfile(file.__str__()):
            os.remove(file.__str__())

        # Update progress bar
        pbar.update(1)



if __name__=='__main__':
    packets_per_session = 10

    # Process ISCX dataset
    iscx_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\ISCX'
    iscx_preprocess(iscx_dataset_path, packets_per_session)

    # Process VNAT-VPN dataset
    vnat_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\VNAT-VPN'
    vnat_preprocess(vnat_dataset_path, packets_per_session)

    print('ALL DONE!!!!!')