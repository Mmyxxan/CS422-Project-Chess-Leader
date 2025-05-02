from chess import Board
from chess import PieceColor
from chess import GameState

def parse_move(move_str):
    """
    Converts move notation (e.g., 'e2 e4') into board indices.
    """
    try:
        start, end = move_str.split()
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])
        return start_row, start_col, end_row, end_col
    except:
        return None

def play_game():
    board = Board()
    current_turn = PieceColor.WHITE  # White moves first

    while True:
        # Print board state
        board.print_board()

        # Check game state
        state, winner = board.get_game_state()
        if state == GameState.CHECKMATE:
            print(f"Checkmate! {winner.name} wins!")
            break
        elif state == GameState.STALEMATE:
            print("Stalemate! It's a draw!")
            break
        elif state == GameState.CHECK:
            print(f"Check! {winner.name} is in danger.")

        # Get user input
        move_str = input(f"{current_turn.name}'s move (e.g., 'e2 e4'): ").strip().lower()
        if move_str == "quit":
            print("Game over.")
            break

        move = parse_move(move_str)
        if not move:
            print("Invalid move format. Use notation like 'e2 e4'. Try again.")
            continue

        start_row, start_col, end_row, end_col = move
        piece = board[start_row][start_col]

        # Validate move
        if piece is None or piece.color != current_turn:
            print("Invalid move. No piece there or not your turn.")
            continue

        valid_moves = piece.get_valid_moves(board.board, board.last_move)
        if not valid_moves[end_row][end_col]:
            print("Illegal move. Try again.")
            continue

        # Execute move
        board.execute_move(piece, end_row, end_col)
        current_turn = PieceColor.BLACK if current_turn == PieceColor.WHITE else PieceColor.WHITE  # Switch turn

if __name__ == "__main__":
    play_game()
