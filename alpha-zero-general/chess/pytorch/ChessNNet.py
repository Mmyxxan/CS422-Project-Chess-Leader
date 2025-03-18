from NeuralNet import NeuralNet
from .NNet import NNet
from utils import *
import torch
import torch.optim as optim
from tqdm import tqdm
import numpy as np
import time
import os
from chess import PieceType, PieceColor
from chess import CastlingSide
from chess import ChessGame

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    'num_channels': 16,
})

class ChessNNet(NeuralNet):
    def preprocess(self, board):
        """
        Get a string representation of board before using it to feed the neural network.
        Input: 
            board: object type of board
        
        Returns:
            the string representation of the object
        """
        # process board, pi, v
        # prepare board
        tensor_board = []
        size = len(board)
        pieces = [PieceType.KING, PieceType.QUEEN, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK, PieceType.PAWN]
        colors = [PieceColor.WHITE, PieceColor.BLACK]
        sides = [CastlingSide.KING_SIDE, CastlingSide.QUEEN_SIDE]

        for color in colors: 
            for piece in pieces:
                piece_channel = [[0 for _ in range(size)] for _ in range(size)] 
                for i in range(size):
                    for j in range(size):
                        if board[i][j].piece_type == piece and board[i][j].color == color:
                            piece_channel[i][j] = 1
                tensor_board.append(piece_channel)
            
            for side in sides:
                if ChessGame.can_castle(board, color, side):
                    castling_channel = [[1 for _ in range(size)] for _ in range(size)] 
                else:
                    castling_channel = [[0 for _ in range(size)] for _ in range(size)] 
                tensor_board.append(castling_channel)      

        return tensor_board

    def __init__(self, game):
        self.nnet = NNet()
        if args.cuda:
            self.nnet.cuda()

    def train(self, examples):
        """
        This function trains the neural network with examples obtained from
        self-play.

        Input:
            examples: a list of training examples, where each example is of form
                      (board, pi, v). pi is the MCTS informed policy vector for
                      the given board, and v is its value. The examples has
                      board in its canonical form.
        """
        optimizer = optim.Adam(self.nnet.parameters())
        for epoch in range(args.epochs):
            print('EPOCH ::: ' + str(epoch + 1))
            self.nnet.train() # ensure dropout and batch norm work correctly
            pi_losses = AverageMeter()
            v_losses = AverageMeter()

            batch_count = int(len(examples) / args.batch_size)
            t = tqdm(range(batch_count), desc='Training Net')

            for _ in t:
                sample_ids = np.random.randint(len(examples), size=args.batch_size)

                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))

                # preprocess first
                boards = [self.preprocess(board) for board in boards]

                # Write code to epresent data with standard input format here
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                if args.cuda:
                    boards, target_pis, target_vs = boards.contiguous().cuda(), target_pis.contiguous().cuda(), target_vs.contiguous().cuda()

                # Forward pass and compute loss
                out_pi, out_v = self.nnet(boards)

                # if one uses the nn.CrossEntropyLoss, 
                # the input must be unnormalized raw value (aka logits), 
                # the target must be class index instead of one hot encoded vectors.
                l_pi = self.nnet.cross_entropy_loss(out_pi, target_pis)
                l_v = self.nnet.mse_loss(out_v, target_vs) # user-defined?

                total_loss = l_pi + l_v

                # Average and record loss for tqdm
                pi_losses.update(l_pi.item(), boards.size(0))
                v_losses.update(l_v.item(), boards.size(0))
                t.set_postfix(Loss_pi=pi_losses, Loss_v=v_losses)

                # compute gradient and do SGD step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def predict(self, board):
        """
        Input:
            board: current board in its canonical form.

        Returns:
            pi: a policy vector for the current board- a numpy array of length
                game.getActionSize
            v: a float in [-1,1] that gives the value of the current board
        """
        # timing
        # start = time.time()

        # preparing input
        # preprocess first
        board = self.preprocess(board.board)
        # board = torch.FloatTensor(np.array(board).astype(np.float64))
        board = torch.FloatTensor(np.array(board).astype(np.float64)).unsqueeze(0)  # Add batch dimension

        if args.cuda: 
            board = board.contiguous().cuda()

        # Renew the shape
        # board = board.view(1, self.board_x, self.board_y)

        # set the module in evaluation mode
        self.nnet.eval()

        with torch.no_grad():
            pi, v = self.nnet(board)

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        # predict remember to normalize policy by softmax
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def save_checkpoint(self, folder, filename):
        """
        Saves the current neural network (with its parameters) in
        folder/filename
        """
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        torch.save({
            'state_dict': self.nnet.state_dict(),
        }, filepath)

    def load_checkpoint(self, folder, filename):
        """
        Loads parameters of the neural network from folder/filename
        """
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise ("No model in path {}".format(filepath))
        map_location = None if args.cuda else 'cpu'
        checkpoint = torch.load(filepath, map_location=map_location)
        self.nnet.load_state_dict(checkpoint['state_dict'])
