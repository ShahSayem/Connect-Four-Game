import numpy as np
import math
import random

# Constants for the board dimensions
ROWS = 6
COLUMNS = 7

# Symbols for player tokens
AI_PLAYER = "O"
HUMAN_PLAYER = "X"

WINDOW_LENGTH = 4
EMPTY = " "

# ANSI escape codes for colors
RESET = "\033[0m"
RED = "\033[91m"

# Function to create the game board
def create_board():
    return np.full((ROWS, COLUMNS), EMPTY)

# Function to print the board
def print_board(board, winning_positions=None):
    print("\n 1 2 3 4 5 6 7")
    print("+-+-+-+-+-+-+-+")
    for r in range(ROWS):
        row = ""
        for c in range(COLUMNS):
            cell = board[r][c]
            if winning_positions and (r, c) in winning_positions:
                row += f"|{RED}{cell}{RESET}"
            else:
                row += f"|{cell}"
        row += "|"
        print(row)
        print("+-+-+-+-+-+-+-+")

# Function to drop a piece into a column
def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY:
            board[row][col] = piece
            return True
    return False

# Function to check for win conditions and return winning positions
def check_winner(board, piece):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True, [(r, c + i) for i in range(4)]
    
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True, [(r + i, c) for i in range(4)]
    
    # Check positively sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True, [(r + i, c + i) for i in range(4)]
    
    # Check negatively sloped diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True, [(r - i, c + i) for i in range(4)]
    
    return False, None

# Function to check if the board is full
def is_draw(board):
    return all(board[0][col] != EMPTY for col in range(COLUMNS))

# Function to evaluate a window for scoring
def evaluate_window(window, piece):
    score = 0
    opp_piece = AI_PLAYER if piece == HUMAN_PLAYER else HUMAN_PLAYER
    
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5
    
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 100
    
    return score

# Function to score the position on the board
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
    is_terminal, _ = check_winner(board, AI_PLAYER) or check_winner(board, HUMAN_PLAYER) or is_draw(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_winner(board, AI_PLAYER)[0]:
                return (None, 1000000)
            elif check_winner(board, HUMAN_PLAYER)[0]:
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
            print(f"\nHUMAN_PLAYER ({HUMAN_PLAYER}), it's your turn!")
            try:
                col = int(input("Enter the column (1-7): ")) - 1
                if col < 0 or col >= COLUMNS:
                    print("Invalid column. Please choose between 1 and 7.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")
                continue
            
            if drop_piece(board, col, HUMAN_PLAYER):
                won, positions = check_winner(board, HUMAN_PLAYER)
                print_board(board, positions if won else None)
                if won:
                    print(f"\nCongratulations! HUMAN_PLAYER ({HUMAN_PLAYER}) wins!")
                    game_over = True
                elif is_draw(board):
                    print("\nIt's a draw!")
                    game_over = True
                turn += 1
            else:
                print("Column is full. Try a different column.")
        
        # AI player turn
        else:
            print(f"\nAI ({AI_PLAYER}) is thinking...")
            col, _ = minimax(board, 6, -math.inf, math.inf, True)
            if drop_piece(board, col, AI_PLAYER):
                won, positions = check_winner(board, AI_PLAYER)
                print_board(board, positions if won else None)
                if won:
                    print(f"\nAI ({AI_PLAYER}) wins!")
                    game_over = True
                elif is_draw(board):
                    print("\nIt's a draw!")
                    game_over = True
                turn += 1


if __name__ == "__main__":
    play_game()
