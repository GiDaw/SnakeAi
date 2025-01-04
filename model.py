import os
import torch
from torch import nn
from torch.utils.data import DataLoader
import torch.optim as optim

# check what to use
device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
print(f"Using {device} device")

# neural neutwork (11 inputs, 1 hiddent layer with 250 neurons, 3 outputs)
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden1 = nn.Linear(11, 250)
        self.act1 = nn.ReLU()
        self.hidden2 = nn.Linear(250, 3)


    def forward(self, x):
        x = self.act1(self.hidden1(x))
        x =self.hidden2(x)
        return x
    
    def save(self, file_name='model.pth'): #saving the model
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

# trainer for neural network
class QTrainer:
    def __init__(self, model, lr, gamma): 
        self.lr = lr
        self.gamma = gamma
        self.model = model
        #optimizer
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr) 
        #loss function
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # converting and normalizing all data for neural network 
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        if len(state.shape) == 1: #if there 1 dimension
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # qvalue = model.predict(current state)
        pred = self.model(state)

        # Qnew = reward + learning rate * max(future state)
        target = pred.clone() 
        for idx in range(len(done)):
            Q_new = reward[idx]
            # if not died
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            #final qvalue
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        #calculating loss function
        loss = self.criterion(target, pred)

        # back propagation for updating weight in neural network
        self.optimizer.zero_grad() 
        loss.backward()
        self.optimizer.step()