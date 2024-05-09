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
import concurrent.futures





def pcap_to_csv(files_batch):

    global files_opened
    global files_closed
    global pbar


    for file in files_batch:

        files_opened = files_opened + 1

        # print('Files Opened = {}'.format(files_opened))
        # print('Files Closed = {}'.format(files_closed))


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

        files_closed = files_closed + 1
        pbar.update(1)





def get_file_batches(files, num_threads):
    items_per_batch = math.ceil(len(files)/num_threads)
    batches = [files[i:i + items_per_batch] for i in range(0, len(files), items_per_batch)]  
    return batches 


if __name__=='__main__':

    files_opened = 0
    files_closed = 0

    

    num_threads = 100
    path = "../../dataset/ISCX"
    files = list(Path(path).rglob('*.pcap'))



    pbar = tqdm(total=len(files), position=0, desc="Files Done : ")





    files_batches = get_file_batches(files, num_threads)


    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(pcap_to_csv, files_batches)

    print('ALL DONE!!!!!')






# def pcap_to_csv(file):
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

#     df = pd.DataFrame(z)
#     df.to_csv(new[:-4] + 'csv', index=False, header=False)
#     z.clear()





# if __name__=='__main__':

#     path = "../../dataset/ISCX"
#     files = list(Path(path).rglob('*.pcap*'))

#     for file in tqdm(files):
#         pcap_to_csv(file)
        
#     print('ALL FILES DONE!!!!')