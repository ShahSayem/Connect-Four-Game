import numpy as np

# Constants for the board dimensions
ROWS = 6
COLUMNS = 7

# Symbols for player tokens
PLAYER_ONE = "X"
PLAYER_TWO = "O"

# Function to create the game board
def create_board():
    return np.full((ROWS, COLUMNS), " ")

# Function to print the board
def print_board(board):
    print("\n 1 2 3 4 5 6 7")
    print("+-+-+-+-+-+-+-+")
    for row in board:
        print("|" + "|".join(row) + "|")
        print("+-+-+-+-+-+-+-+")

# Function to drop a piece into a column
def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = piece
            return True
    return False

# Check for win conditions
def check_winner(board, piece):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    
    # Check positively sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    
    # Check negatively sloped diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    
    return False

# Function to check if the board is full
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    print("Welcome to Connect Four!\n")
    print_board(board)
    
    turn = 0
    game_over = False
    
    while not game_over:
        # Determine current player
        if turn % 2 == 0:
            piece = PLAYER_ONE
            print("\nPlayer 1 (X), it's your turn!")
        else:
            piece = PLAYER_TWO
            print("\nPlayer 2 (O), it's your turn!")
        
        # Ask for a column input
        try:
            col = int(input("Enter the column (1-7): ")) - 1
            if col < 0 or col >= COLUMNS:
                print("Invalid column. Please choose between 1 and 7.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
            continue
        
        # Drop the piece if the move is valid
        if drop_piece(board, col, piece):
            print_board(board)
            if check_winner(board, piece):
                print(f"\nCongratulations! Player {1 if piece == PLAYER_ONE else 2} ({piece}) wins!")
                game_over = True
            elif is_draw(board):
                print("\nIt's a draw!")
                game_over = True
            turn += 1
        else:
            print("Column is full. Try a different column.")
    
# Start the game
if __name__ == "__main__":
    play_game()
