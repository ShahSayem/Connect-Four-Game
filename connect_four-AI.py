import numpy as np
import math
import random

# Constants for the board dimensions
ROWS = 6
COLUMNS = 7

# Symbols for player tokens
PLAYER_ONE = "X"
PLAYER_TWO = "O"
AI_PLAYER = PLAYER_TWO
HUMAN_PLAYER = PLAYER_ONE

WINDOW_LENGTH = 4
EMPTY = " "

# Function to create the game board
def create_board():
    return np.full((ROWS, COLUMNS), EMPTY)

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
        if board[row][col] == EMPTY:
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
    return all(board[0][col] != EMPTY for col in range(COLUMNS))

# Evaluate window for scoring
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_ONE if piece == PLAYER_TWO else PLAYER_TWO
    
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    
    return score

# Score the position on the board
def score_position(board, piece):
    score = 0
    
    # Score center column
    center_array = [board[r][COLUMNS // 2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3
    
    # Score horizontal
    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLUMNS)]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    
    # Score vertical
    for c in range(COLUMNS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    
    # Score positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    
    # Score negative diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    
    return score

# Check if a column is valid to play
def is_valid_location(board, col):
    return board[0][col] == EMPTY

# Get the next open row in a column
def get_next_open_row(board, col):
    for r in reversed(range(ROWS)):
        if board[r][col] == EMPTY:
            return r

# Minimax function with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = [c for c in range(COLUMNS) if is_valid_location(board, c)]
    is_terminal = check_winner(board, PLAYER_ONE) or check_winner(board, PLAYER_TWO) or is_draw(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_winner(board, AI_PLAYER):
                return (None, 1000000)
            elif check_winner(board, HUMAN_PLAYER):
                return (None, -1000000)
            else:  # Draw
                return (None, 0)
        else:
            return (None, score_position(board, AI_PLAYER))
    
    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board[row][col] = AI_PLAYER
            new_score = minimax(board, depth - 1, alpha, beta, False)[1]
            board[row][col] = EMPTY
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board[row][col] = HUMAN_PLAYER
            new_score = minimax(board, depth - 1, alpha, beta, True)[1]
            board[row][col] = EMPTY
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# Main game loop
def play_game():
    board = create_board()
    print("Welcome to Connect Four with AI!\n")
    print_board(board)
    
    turn = 0
    game_over = False
    
    while not game_over:
        # Human player turn
        if turn % 2 == 0:
            print("\nPlayer 1 (X), it's your turn!")
            try:
                col = int(input("Enter the column (1-7): ")) - 1
                if col < 0 or col >= COLUMNS:
                    print("Invalid column. Please choose between 1 and 7.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")
                continue
            
            if drop_piece(board, col, HUMAN_PLAYER):
                print_board(board)
                if check_winner(board, HUMAN_PLAYER):
                    print("\nCongratulations! Player 1 (X) wins!")
                    game_over = True
                elif is_draw(board):
                    print("\nIt's a draw!")
                    game_over = True
                turn += 1
            else:
                print("Column is full. Try a different column.")
        
        # AI player turn
        else:
            print("\nAI (O) is thinking...")
            col, _ = minimax(board, 5, -math.inf, math.inf, True)
            if drop_piece(board, col, AI_PLAYER):
                print_board(board)
                if check_winner(board, AI_PLAYER):
                    print("\nAI (O) wins!")
                    game_over = True
                elif is_draw(board):
                    print("\nIt's a draw!")
                    game_over = True
                turn += 1

if __name__ == "__main__":
    play_game()
