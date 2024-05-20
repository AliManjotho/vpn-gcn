import numpy as np
import os
import json
from pathlib import Path
from tqdm import tqdm
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
import torch


def generate_graph(dataset_path):

    # Get list of all PCAP session file paths
    files = list(Path(dataset_path).rglob('*.json'))
    pbar = tqdm(total=len(files), desc='Files Done: ')

    graph_list = []
    for file_number, file in enumerate(files):

        with open(file.__str__(), 'r') as file_handle:
            json_data = json.load(file_handle)
            
            id = json_data["id"]
            features = json_data["features"]
            edge_indices = json_data["edge_indices"]
            class_label = json_data["class"]
            class_vector = json_data["class_vector"]

            edge_index = torch.from_numpy(np.array(edge_indices))
            x = torch.from_numpy(np.array(features))
            y = torch.from_numpy(np.array(class_vector))
            graph = Data(x=x, edge_index=edge_index.T, y=y)

            graph_list.append(graph)
            
        pbar.update(1)

    print(len(graph_list))



        


if __name__=='__main__':

    # Generate graphs for ISCX dataset
    iscx_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\ISCX'
    generate_graph(iscx_dataset_path)

    # Process VNAT-VPN dataset
    # vnat_dataset_path = r'D:\SH\TrafficClassification\vpn-gcn\datasets\VNAT-VPN'
    # generate_graph(vnat_dataset_path)


    print('ALL DONE!!!!!')
