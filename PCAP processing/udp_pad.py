#This code Pads UDP headers with zeros to match TCP header length of 20
from scapy.all import *
from scapy.utils import PcapWriter
import glob
from scapy.compat import raw
from scapy.layers.inet import IP, UDP
from scapy.packet import Padding
from pathlib import Path
from tqdm import tqdm


# def udp_pad(thread_index, file):

#     print('Thread {} started!'.format(thread_index))

#     packet_list = rdpcap(file.__str__())
#     new = PcapWriter(file.__str__())

#     for packet in packet_list:
#         if UDP in packet:
#             layer_after = packet[UDP].payload.copy()

#             pad = Padding()
#             pad.load = '\x00' * 12

#             layer_before = packet.copy()
#             layer_before[UDP].remove_payload()
#             j = layer_before / raw(pad) / layer_after

#             new.write(j)
#         else:
#             new.write(packet)
            
#     new.close()
#     print(file.name + ' done!!!!!')



# def main():

#     path = "../../dataset/ISCX"
#     files = Path(path).rglob('*.pcap*')

#     thread_index = 1
#     for file in files:
#         thread = Thread(target=udp_pad, args=(thread_index, file))
#         thread.start()
#         thread_index = thread_index + 1




def udp_pad(file):
    packet_list = rdpcap(file.__str__())
    new = PcapWriter(file.__str__())

    for packet in packet_list:
        if UDP in packet:
            layer_after = packet[UDP].payload.copy()

            pad = Padding()
            pad.load = '\x00' * 12

            layer_before = packet.copy()
            layer_before[UDP].remove_payload()
            j = layer_before / raw(pad) / layer_after

            new.write(j)
        else:
            new.write(packet)
            
    new.close()



    

if __name__=='__main__':

    path = "../../dataset/ISCX"
    files = list(Path(path).rglob('*.pcap*'))

    for file in tqdm(files):
        udp_pad(file)
        
    print('ALL FILES DONE!!!!')

