import os
import torch
from torch.nn import Linear
from torch_geometric.nn import GCNConv
from torch_geometric.nn import global_mean_pool
from pcapdataset import *
import math
from torch.nn import Linear, BatchNorm1d
import torch.nn.functional as F
from torch_geometric.loader import DataLoader, ImbalancedSampler
from torch_geometric.nn import GCNConv, GATConv, TopKPooling, BatchNorm, GraphConv
from torch_geometric.nn import global_mean_pool as gap, global_max_pool as gmp
from pcapdataset import PCAPDataset
from gcnmodel import GCN

def train(model):
    model.train()

    for data in train_loader:  # Iterate in batches over the training dataset.
         data.to(device)
         out = model(data)  # Perform a single forward pass.
         loss = criterion(out, data.y)  # Compute the loss.
         loss.backward()  # Derive gradients.
         optimizer.step()  # Update parameters based on gradients.
         optimizer.zero_grad()  # Clear gradients.

def test(loader):
     model.eval()

     correct = 0
     for data in loader:  # Iterate in batches over the training/test dataset.
         data.to(device)
         out = model(data)  
         pred = out.argmax(dim=1)  # Use the class with highest probability.
         correct += int((pred == data.y.argmax(dim=1)).sum())  # Check against ground-truth labels.
     return correct / len(loader.dataset)  # Derive ratio of correct predictions.



    
if __name__=='__main__':

    epochs = 150
    batch_size = 1024

    iscx_root = r'D:\SH\TrafficClassification\vpn-gcn\datasets\iscx'
    dataset = PCAPDataset(root=iscx_root)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    torch.manual_seed(12345)
    dataset = dataset.shuffle()

    train_dataset = dataset[:math.floor(len(dataset)/7)]
    test_dataset = dataset[math.floor(len(dataset)/7):]

    print(f'Number of training graphs: {len(train_dataset)}')
    print(f'Number of test graphs: {len(test_dataset)}')

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    print(f'Number of training classes: {train_dataset.num_classes}')
    print(f'Number of test classes : {test_dataset.num_classes}')

    model = GCN(dataset.num_classes, dataset.num_features).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = torch.nn.CrossEntropyLoss()

    for epoch in range(1, epochs+1):
        train(model)
        train_acc = test(train_loader)
        test_acc = test(test_loader)
        print(f'Epoch: {epoch:03d}, Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}')
        # print('Memory Allocated = ' + str(torch.cuda.memory_allocated()/1024/1024/1024))
        # print('Memory Cached = ' + str(torch.cuda.memory_cached()/1024/1024/1024))

    torch.save(model.state_dict(), 'model_weights.pth')