import torch
import torch.nn as nn
from NNetLayer import ConvolutionalLayer, ResidualBlock, PolicyHead, ValueHead

class NNet(nn.Module):
    """
    The neural network for Alpha Zero:
    - Input: 8x8x16 
    (8x8 board, 12 for each color, type of piece + 4 castling for each side, each color)
    - Output: policy head (probabilities for each move), value head (game result)
    The neural network architecture:
    - 
    """
    INPUT_CHANNELS = 16
    NUM_FILTERS = 128
    NUM_RESIDUAL_BLOCKS = 10

    def __init__(self):
        super().__init__()
        self.convolutional_layer = ConvolutionalLayer(input_channels=self.INPUT_CHANNELS, num_filters=self.NUM_FILTERS)
        self.residual_blocks = [ResidualBlock(self.NUM_FILTERS) for _ in range(self.NUM_RESIDUAL_BLOCKS)]
        self.policy_head = PolicyHead(self.NUM_FILTERS)
        self.value_head = ValueHead(self.NUM_FILTERS)
        self.softmax = nn.Softmax(1)
        self.mse_loss = nn.MSELoss()
        self.cross_entropy_loss = nn.CrossEntropyLoss()

    def forward(self, x):
        x = self.convolutional_layer(x)
        for block in self.residual_blocks:
            x = block(x)
        policy = self.policy_head(x)
        value = self.value_head(x)

        policy_softmax = self.softmax(policy)

        return policy_softmax, value

