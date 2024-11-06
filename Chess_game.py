import random

# Initialize board with a simple ASCII representation
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

# Function to display the board with notations
def print_board(board):
    print("  a b c d e f g h")  # File notation
    for i in range(8):
        # Print each rank with pieces, adding row numbers (8 to 1)
        print(f"{8 - i} " + " ".join(board[i]) + f" {8 - i}")
    print("  a b c d e f g h")  # File notation again at the bottom
    print()

# Function to check if a piece's movement is valid
def is_valid_piece_move(board, piece, start_row, start_col, end_row, end_col):
    row_diff = end_row - start_row
    col_diff = end_col - start_col

    if piece.lower() == 'p':  # Pawn
        direction = 1 if piece.islower() else -1  # Down for black, up for white
        if col_diff == 0:  # Moving forward
            if row_diff == direction and board[end_row][end_col] == ".":
                return True
            elif row_diff == 2 * direction and start_row in (1, 6) and board[end_row][end_col] == ".":
                return True
        elif abs(col_diff) == 1 and row_diff == direction:  # Capturing
            return board[end_row][end_col] != "." and board[end_row][end_col].islower() != piece.islower()
    elif piece.lower() == 'r':  # Rook
        if row_diff == 0 or col_diff == 0:
            return not any(board[start_row + i * (row_diff // abs(row_diff))][start_col + i * (col_diff // abs(col_diff))]
                           for i in range(1, max(abs(row_diff), abs(col_diff))))
    elif piece.lower() == 'n':  # Knight
        return abs(row_diff) == 2 and abs(col_diff) == 1 or abs(row_diff) == 1 and abs(col_diff) == 2
    elif piece.lower() == 'b':  # Bishop
        if abs(row_diff) == abs(col_diff):
            return not any(board[start_row + i * (row_diff // abs(row_diff))][start_col + i * (col_diff // abs(col_diff))]
                           for i in range(1, abs(row_diff)))
    elif piece.lower() == 'q':  # Queen
        if row_diff == 0 or col_diff == 0:  # Rook-like movement
            return not any(board[start_row + i * (row_diff // abs(row_diff))][start_col + i * (col_diff // abs(col_diff))]
                           for i in range(1, max(abs(row_diff), abs(col_diff))))
        elif abs(row_diff) == abs(col_diff):  # Bishop-like movement
            return not any(board[start_row + i * (row_diff // abs(row_diff))][start_col + i * (col_diff // abs(col_diff))]
                           for i in range(1, abs(row_diff)))
    elif piece.lower() == 'k':  # King
        return abs(row_diff) <= 1 and abs(col_diff) <= 1

    return False

# Function to check if a king is in check
def is_in_check(board, king_position, is_white):
    king_row, king_col = king_position
    opponent_pieces = "prnbqk" if is_white else "PRNBQK"

    for row in range(8):
        for col in range(8):
            if board[row][col] in opponent_pieces and is_valid_piece_move(board, board[row][col], row, col, king_row, king_col):
                return True
    return False

# Function to find king position
def find_king_position(board, is_white):
    king = 'K' if is_white else 'k'
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                return (row, col)
    return None

# Function to validate a move and update the board
def make_move(board, move, is_white_turn=True):
    if len(move) != 4:
        print("Invalid move format. Please use UCI format (e.g., e2e4).")
        return False

    try:
        start, end = move[:2], move[2:]
        start_row, start_col = 8 - int(start[1]), ord(start[0]) - ord('a')
        end_row, end_col = 8 - int(end[1]), ord(end[0]) - ord('a')

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            print("Invalid move: Position out of bounds.")
            return False

        piece = board[start_row][start_col]
        if piece == ".":
            print("Invalid move: No piece at starting position.")
            return False
        if piece.isupper() != is_white_turn:
            print("Invalid move: Wrong turn.")
            return False
        if not is_valid_piece_move(board, piece, start_row, start_col, end_row, end_col):
            print("Invalid move: Piece cannot move in that way.")
            return False

        # Make the move
        captured_piece = board[end_row][end_col]
        board[end_row][end_col] = piece
        board[start_row][start_col] = "."

        # Check if move puts own king in check
        king_position = find_king_position(board, is_white_turn)
        if is_in_check(board, king_position, is_white_turn):
            print("Invalid move: Move puts king in check.")
            # Undo move if king is in check
            board[start_row][start_col] = piece
            board[end_row][end_col] = captured_piece
            return False

        return True
    except (IndexError, ValueError):
        print("Invalid move format. Please use UCI format (e.g., e2e4).")
        return False

# Function to randomly move for the computer (only for pawns here for simplicity)
def computer_move(board):
    while True:
        start_col = random.choice(range(8))
        start_row = 1  # Only moving black pawns for simplicity
        end_row = start_row + 1
        
        if board[start_row][start_col] == "p" and board[end_row][start_col] == ".":
            board[end_row][start_col] = "p"
            board[start_row][start_col] = "."
            print(f"Computer moves: {chr(start_col + ord('a'))}{8 - start_row}{chr(start_col + ord('a'))}{8 - end_row}")
            break

# Main game loop
def main():
    print("Welcome to Basic Python Chess!")
    print("1. Play with Friend")
    print("2. Play with Computer")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice not in {"1", "2"}:
        print("Invalid choice.")
        return
    
    print_board(board)
    turn = "white"
    
    while True:
        if choice == "1" or (choice == "2" and turn == "white"):
            move = input(f"{turn.capitalize()}'s move (e.g., e2e4): ")
            if make_move(board, move, is_white_turn=(turn == "white")):
                print_board(board)
                turn = "black" if turn == "white" else "white"
        elif choice == "2" and turn == "black":
            computer_move(board)
            print_board(board)
            turn = "white"

if __name__ == "__main__":
    main()
