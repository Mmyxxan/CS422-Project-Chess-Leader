import torch
from chess.pytorch.NNet import NNet
nnet = NNet()
x = torch.randn(1, 16, 8, 8)  # Simulated input
policy, value = nnet(x)
print(policy.shape, value.shape)
