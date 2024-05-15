#This code removes the ethernet header of PCAP files
from scapy.all import *
import glob
import numpy as np
import pandas as pd
from scapy.compat import raw
from pathlib import Path
from tqdm import tqdm
import concurrent.futures
import os



def remove_ethernet(files_batch):

    global pbar

    for file in files_batch:

        packet_list = rdpcap(file.__str__())
        new = PcapWriter(file.__str__())

        for packet in packet_list:

            if Ether in packet:
                payload = packet[Ether].payload
                new.write(payload)
            else:
                new.write(packet)

        new.close()
        pbar.update(1)



def get_file_batches(files, num_threads):
    items_per_batch = math.ceil(len(files)/num_threads)
    batches = [files[i:i + items_per_batch] for i in range(0, len(files), items_per_batch)]  
    return batches 


if __name__=='__main__':

    num_threads = 100
    path = "../../dataset/ISCX"
    files = list(Path(path).rglob('*.pcap'))

    pbar = tqdm(total=len(files), position=0, desc="Files Done : ")
    files_batches = get_file_batches(files, num_threads)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(remove_ethernet, files_batches)

    print('ALL DONE!!!!!')