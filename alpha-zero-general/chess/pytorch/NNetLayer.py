import torch
import torch.nn as nn

class ConvolutionalLayer(nn.Module):
    def __init__(self, input_channels, num_filters):
        """
        The convolutional layer contains 128 3x3 filter
        with batch normalization followed by ReLU activation
        """
        super().__init__()
        self.conv = nn.Conv2d(in_channels=input_channels, out_channels=num_filters, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(num_features=num_filters)
        self.relu = nn.ReLU()

    def forward(self, x):
        """
        Returns the output with input x
        """
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)

        return x
    
class ResidualBlock(nn.Module):
    def __init__(self, num_filters):
        """
        The residual block maps x to F(x) + x contains 2 convolutional layer
        """
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=num_filters, out_channels=num_filters, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(num_features=num_filters)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(in_channels=num_filters, out_channels=num_filters, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(num_features=num_filters)
        self.relu2 = nn.ReLU()

    def forward(self, x):
        input = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x += input
        x = self.relu2(x)

        return x
    
class PolicyHead(nn.Module):
    def __init__(self, input_channels):
        """
        The policy head for the alpha zero's neural network
        """
        super().__init__()
        self.conv = nn.Conv2d(in_channels=input_channels, out_channels=2, kernel_size=1)
        self.bn = nn.BatchNorm2d(2)
        self.relu = nn.ReLU()
        self.fc = nn.Linear(64 * 2, 64 * 73)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        x = x.view(x.shape[0], 64 * 2)
        x = self.fc(x)

        return x
    
class ValueHead(nn.Module):
    """
        The value head for the alpha zero's neural network
    """
    def __init__(self, input_channels):
        super().__init__()
        self.conv = nn.Conv2d(in_channels=input_channels, out_channels=1, kernel_size=1)
        self.bn = nn.BatchNorm2d(1)
        self.relu1 = nn.ReLU()
        self.fc1 = nn.Linear(64, 256)
        self.relu2 = nn.ReLU()
        self.fc2 = nn.Linear(256, 1)
        self.tanh = nn.Tanh()
    
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu1(x)

        x = x.view(x.shape[0], -1)  # Flatten to (batch_size, 64)

        x = self.fc1(x)
        x = self.relu2(x)
        x = self.fc2(x)
        x = self.tanh(x)

        return x
