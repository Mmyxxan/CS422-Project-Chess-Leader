from torch.utils.data import random_split
from alpha_zero_chess.Dataset import PGNDataset
from torch.utils.data import DataLoader
from alpha_zero_chess.ChessNNet import ChessNNet
from alpha_zero_chess.utils import dotdict
import torch

args = dotdict({
    'epochs': 40,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    'folder': 'model/',
    'filename': 'chess_nnet_ccrl.pth',
    'max_games_training': 70000,
    'max_games_debugging': 20
})

dataset = PGNDataset("D:/y3t2/CCRL-404.[1542299].pgn/CCRL.pgn", max_games=args['max_games_debugging'])
train_size = int(0.9 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=args['batch_size'], shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=args['batch_size'])

trainer = ChessNNet(args)
trainer.train(train_loader, val_loader)

# import chess.pgn
# import io

# def count_games(pgn_path):
#     with open(pgn_path, "rb") as f_raw:
#         # Decode with BOM-safe utf-8-sig and wrap in StringIO
#         text = f_raw.read().decode("utf-8-sig")
#         f = io.StringIO(text)

#         count = 0
#         while True:
#             game = chess.pgn.read_game(f)
#             if game is None:
#                 break
#             count += 1
#         return count

# # Usage
# pgn_file = "D:/y3t2/CCRL-404.[1542299].pgn/CCRL.pgn"
# print("Total games in PGN file:", count_games(pgn_file))

