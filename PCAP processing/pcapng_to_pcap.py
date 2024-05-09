import os
from os.path import join
import string
from pathlib import Path


path = "../../dataset/ISCX"
files = Path(path).rglob('*.pcap*')
count = 0


for file in files:
    old_file = file.resolve().__str__()
    new_file = old_file.replace("pcapng", "pcap")

    if old_file[-7:len(old_file)] == '.pcapng':
        command = "editcap -F libpcap -T ether " + old_file + " " + new_file
        os.system(command)
        command = "del " + old_file
        os.system(command)
        count = count + 1
        print("File converted : ", new_file)

print(" ================================================")
print(" DONE.")
print(" Number of Pcap changed to Pcapng  : ", count)
print(" =================================================")