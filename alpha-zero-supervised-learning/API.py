from flask import Flask, request, jsonify
import chess
from arena_players import AlphaZeroPlayer, nnet_args, args, ChessGame, move_index
import numpy as np

app = Flask(__name__)

game = ChessGame.ChessGame()
alpha_zero_player = AlphaZeroPlayer(game)

def encode_to_FEN_from_data(data):
    pass

@app.route('/move', methods=['POST'])
def get_move():
    data = request.json

    fen = data.get('fen')
    difficulty = data.get('difficulty', 'medium').lower()

    if not fen:
        return jsonify({'error': 'FEN string is required.'}), 400

    try:
        board = chess.Board(fen)
    except Exception as e:
        return jsonify({'error': f'Invalid FEN string: {str(e)}'}), 400

    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({'error': 'Difficulty must be easy, medium, or hard.'}), 400

    action_index = alpha_zero_player.play(board, 1 if board.turn == chess.WHITE else -1)

    move = move_index.index_to_move(action_index, board)

    from_square = move.from_square  # 0-63 integer
    to_square = move.to_square      # 0-63 integer

    from_row = 7 - (from_square // 8)
    from_col = from_square % 8

    to_row = 7 - (to_square // 8)
    to_col = to_square % 8

    return jsonify({
        'PlayerMove': {
            'initialPosition': {
                'x': from_row,
                'y': from_col
            },
            'destinationPosition': {
                'x': to_row,
                'y': to_col
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
