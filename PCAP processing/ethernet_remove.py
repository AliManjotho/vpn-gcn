#This code removes the ethernet header of PCAP files
from scapy.all import *
from scapy.utils import PcapWriter
from scapy.layers.l2 import Ether
from pathlib import Path
from tqdm import tqdm




# def remove_ethernet(thread_index, file):

#     print('Thread {} started!'.format(thread_index))

#     packet_list = rdpcap(file.__str__())
#     new = PcapWriter(file.__str__())

#     for packet in packet_list:

#         if Ether in packet:
#             payload = packet[Ether].payload
#             new.write(payload)
#         else:
#             new.write(packet)

#     new.close()
#     print(file.name + ' done!!!!!')



# def main():

#     path = "../../dataset/ISCX"
#     files = list(Path(path).rglob('*.pcap*'))

#     thread_index = 1
#     for file in files:
#         thread = Thread(target=remove_ethernet, args=(thread_index, file))
#         thread.start()
#         thread_index = thread_index + 1

#     thread_index = 1
#     for file in tqdm(files):
#         remove_ethernet(thread_index, file)
#         thread_index = thread_index + 1



def remove_ethernet(file):
    packet_list = rdpcap(file.__str__())
    new = PcapWriter(file.__str__())

    for packet in packet_list:

        if Ether in packet:
            payload = packet[Ether].payload
            new.write(payload)
        else:
            new.write(packet)

    new.close()

    


if __name__=='__main__':

    path = "../../dataset/ISCX"
    files = list(Path(path).rglob('*.pcap*'))
    
    for file in tqdm(files):
        remove_ethernet(file)

    print('ALL FILES DONE!!!!')