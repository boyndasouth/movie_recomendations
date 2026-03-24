import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as mp

class MovieRecNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9, 14)
        self.fc2 = nn.Linear(14, 8)
        self.out = nn.Linear(8, 7)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)
    
torch.manual_seed(173)
movies = pd.read_csv('movies.csv')
model = MovieRecNN()
movies['genre'] = movies['genre'].replace('Action', 0)
movies['genre'] = movies['genre'].replace('Comedy', 1)
movies['genre'] = movies['genre'].replace('Drama', 2)
movies['genre'] = movies['genre'].replace('Horror', 3)
movies['genre'] = movies['genre'].replace('Romance', 4)
movies['genre'] = movies['genre'].replace('SciFi', 5)
movies['genre'] = movies['genre'].replace('Thriller', 6)


criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

X = movies.drop('genre', axis=1).values
y = movies['genre'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.25, 
                                                    random_state=52)

X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)
y_train = mp.array(y_train, dtype=mp.float32) 
y_test = mp.array(y_test, dtype=mp.float32) 

y_train = torch.LongTensor(y_train)
y_test = torch.LongTensor(y_test)

losses = []
epochs = 500

for i in range(epochs):
    y_pred = model(X_train)
    loss = criterion(y_pred, y_train)

    losses.append(loss.detach().numpy())
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def film_nn(age,
            likes_explosions,
            likes_romance,
            likes_scary,
            likes_deep_story,
            likes_humor,
            likes_space,
            likes_mystery,
            preferred_length):
    with torch.no_grad():
        new_genre = model(torch.tensor([age,
                                        likes_explosions,
                                        likes_romance,
                                        likes_scary,
                                        likes_deep_story,
                                        likes_humor,
                                        likes_space,
                                        likes_mystery,
                                        preferred_length], 
                                        dtype=torch.float32))
        genres = torch.softmax(new_genre, dim=0)
        top3_values, top3_indices = torch.topk(genres, k=3, dim=0)
        return top3_indices.tolist()
    
    