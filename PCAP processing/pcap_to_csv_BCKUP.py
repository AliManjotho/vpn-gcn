# This code takes every PCAP file, converts it to raw packet (byte value)
# then converts the raw byte to decimal and normalises it to fall between 0 - 1
# it pads every packet to have a max length of 1500 and finally converts it to CSV format

from scapy.all import *
import glob
import numpy as np
import pandas as pd
from scapy.compat import raw
from pathlib import Path
from tqdm import tqdm




# def pcap_to_csv(thread_index, file):

#     print('Thread {} started!'.format(thread_index))

#     z = []
#     max = 1500
#     packet_list = rdpcap(file.__str__())
#     new = file.__str__()

#     for packet in packet_list:
#         t = np.frombuffer(raw(packet), dtype=np.uint8)[0: max] / 255
#         if len(t) <= max:
#             pad_width = max - len(t)
#             t = np.pad(t, pad_width=(0, pad_width), constant_values=0)
#             z.append(t)
            
#     if new[-7:len(new)] == '.pcapng':
#         new = new[:-7]
#         print(new)
#     else:
#         new = new[:-5]
#         print(new)

#     df = pd.DataFrame(z)
#     df.to_csv(new + '.csv', index=False, header=False)
#     z.clear()

#     print(file.name + ' done!!!!!')



# def main():

#     path = "../../dataset/ISCX"
#     files = Path(path).rglob('*.pcap*')

#     thread_index = 1
#     for file in files:
#         thread = Thread(target=pcap_to_csv, args=(thread_index, file))
#         thread.start()
#         thread_index = thread_index + 1






def pcap_to_csv(file):
    z = []
    max = 1500
    packet_list = rdpcap(file.__str__())
    new = file.__str__()

    for packet in packet_list:
        t = np.frombuffer(raw(packet), dtype=np.uint8)[0: max] / 255
        if len(t) <= max:
            pad_width = max - len(t)
            t = np.pad(t, pad_width=(0, pad_width), constant_values=0)
            z.append(t)

    df = pd.DataFrame(z)
    df.to_csv(new[:-4] + 'csv', index=False, header=False)
    z.clear()





if __name__=='__main__':

    path = "../../dataset/ISCX"
    files = list(Path(path).rglob('*.pcap*'))

    for file in tqdm(files):
        pcap_to_csv(file)
        
    print('ALL FILES DONE!!!!')