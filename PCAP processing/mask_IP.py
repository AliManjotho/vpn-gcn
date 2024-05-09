# This code will replace all IPv4 and IPv6 addresses with zeros
from scapy.all import *
from scapy.layers.inet6 import IPv6
from scapy.utils import PcapWriter
import glob
from scapy.layers.inet import IP, UDP
from pathlib import Path
from tqdm import tqdm



# def mask_ips(thread_index, file):

#     print('Thread {} started!'.format(thread_index))

#     packet_list = rdpcap(file.__str__())
#     new = PcapWriter(file.__str__())

#     for packet in packet_list:
#         if IPv6 in packet:
#             packet[IPv6].dst = '0000::0:0'
#             packet[IPv6].src = '0000::0000:0000:0000:0000'
#             new.write(packet)
#         if IP in packet:
#             packet[IP].dst = '0.0.0.0'
#             packet[IP].src = '0.0.0.0'
#             new.write(packet)
            
#     new.close()
#     print(file.name + ' done!!!!!')



# def main():

#     path = "../../dataset/ISCX"
#     files = Path(path).rglob('*.pcap*')

#     thread_index = 1
#     for file in files:
#         thread = Thread(target=mask_ips, args=(thread_index, file))
#         thread.start()
#         thread_index = thread_index + 1






def mask_ips(file):
    packet_list = rdpcap(file.__str__())
    new = PcapWriter(file.__str__())

    for packet in packet_list:
        if IPv6 in packet:
            packet[IPv6].dst = '0000::0:0'
            packet[IPv6].src = '0000::0000:0000:0000:0000'
            new.write(packet)
        if IP in packet:
            packet[IP].dst = '0.0.0.0'
            packet[IP].src = '0.0.0.0'
            new.write(packet)
            
    new.close()



    



if __name__=='__main__':

    path = "../../dataset/ISCX"
    files = list(Path(path).rglob('*.pcap*'))

    for file in tqdm(files):
        mask_ips(file)

    print('ALL FILES DONE!!!!')
