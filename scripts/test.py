import numpy as np
import os
import json
from pathlib import Path

iscx_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\ISCX'
# file = r'D:\SH\TrafficClassification\vpn-gcn\datasets\ISCX\00000001.json'

files = list(Path(iscx_dataset_path).rglob('*.json'))

for file in files:
    with open(file.__str__(), 'r') as file_handle:
        json_data = json.load(file_handle)

    print(json_data["id"])
    print(file)
    file_handle.close()