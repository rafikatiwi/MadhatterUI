import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.optim.lr_scheduler as scheduler
from torch.utils.data import DataLoader, Dataset
import json
from Models.Models import AutoEncoder

class VectorDataset(Dataset):
    """
    reads user or item vector datasets
    """
    def __init__(self, file_path):
        with open(file_path, 'r') as fp:
            self.data = json.load(fp)
            self.key = list(self.data.keys())
            
    def __getitem__(self, index):
        data = self.data[self.key[index]]
        data1 = torch.Tensor(data)
        #data1 = self.normalize_data(data1)
        #data2 = torch.Tensor(data[143:])
        #data2 = self.normalize_data(data2)
        #data = torch.cat((data1, data2))
        return data1
    
    def normalize_data(self, data):
        data = F.normalize(data, dim=0)
        return data
        
    def __len__(self):
        data_len = len(self.key)
        return data_len
    

test = VectorDataset('./datasets/item_vectors_tf_idf.json')


num_epochs = 4000
batch_size = 143
learning_rate = 0.1
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

dataset = test
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4)

model = AutoEncoder(input_len=143, hidden_unit=10).to(device)
criterion = nn.SmoothL1Loss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate, weight_decay=1e-5)
scheduler = scheduler.MultiStepLR(optimizer, [1000, 2000, 3000], gamma=0.25)

loss = []

for epoch in range(num_epochs):
    running_loss = 0.0
    for data in dataloader:
        scheduler.step()
        data = data.to(device)
        # ===================forward=====================
        output = model(data)
        loss = criterion(output, data)
        # ===================backward====================
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    # ===================log========================
    print('epoch [{}/{}], loss:{:.8f}'
          .format(epoch + 1, num_epochs, running_loss/143))
    
    
torch.save(model.state_dict(), './trained_model/item_encoder.pth')