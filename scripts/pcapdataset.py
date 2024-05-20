import torch
import os
import os.path as osp
import pandas as pd
from torch_geometric.data import InMemoryDataset, Dataset, Data
from torch_geometric.utils.convert import to_networkx
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
import torch_geometric.transforms as T
from pathlib import Path
import json
import numpy as np
from utils import *


class PCAPDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None):
        super(PCAPDataset, self).__init__(root, transform, pre_transform, pre_filter)


    @property
    def raw_file_names(self):
        raw_files = list(Path(self.root + '\\raw').rglob('*.json'))
        return [item.name for item in raw_files]

    @property
    def processed_file_names(self):
        raw_files = list(Path(self.root + '\\raw').rglob('*.json'))
        processed_files = ['data_' + str(i) + '.pt' for i in range(1,len(raw_files)+1)]    
        return processed_files
    
    def download(self):
        pass

    def process(self):

        pbar = tqdm(total=len(self.raw_paths), desc='Files Done: ')

        graph_list = []
        for file_number, raw_file in enumerate(self.raw_paths):

            with open(raw_file, 'r') as file_handle:
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

                torch.save(graph, os.path.join(self.processed_dir, 'data_' + str(file_number) + '.pt'))

            pbar.update(1)

    def len(self):
        return len(self.processed_file_names)
    
    def get(self, idx):
        data = torch.load(os.path.join(self.processed_dir, 'data_' + str(idx) + '.pt'))
        return data

        



if __name__=='__main__':

    iscx_root = r'D:\SH\TrafficClassification\vpn-gcn\datasets\data\iscx'
    iscx_dataset = PCAPDataset(root=iscx_root)

    print(iscx_dataset[5].num_nodes)



    # vnat_root = r'D:\SH\TrafficClassification\vpn-gcn\datasets\data\vnat'
    # vnat_dataset = PCAPDataset(root=vnat_root)


