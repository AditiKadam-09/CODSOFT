import streamlit as st
import numpy as np

# Initialize session state variables
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)
if 'player' not in st.session_state:
    st.session_state.player = 1  # Human starts first (X)
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Medium"
if 'winner' not in st.session_state:
    st.session_state.winner = None

# Function to check for a winner
def check_win(board):
    for i in range(3):
        if np.all(board[i, :] == board[i, 0]) and board[i, 0] != 0:
            return board[i, 0]
        if np.all(board[:, i] == board[0, i]) and board[0, i] != 0:
            return board[0, i]
    if board[0, 0] == board[1, 1] == board[2, 2] != 0:
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] != 0:
        return board[0, 2]
    return 0

# Minimax Algorithm
def minimax(board, depth, is_maximizing, alpha=-np.inf, beta=np.inf):
    winner = check_win(board)
    if winner == 2:  # AI wins
        return 10 - depth
    if winner == 1:  # Human wins
        return depth - 10
    if np.all(board != 0):  # Draw
        return 0

    if is_maximizing:
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board[i, j] = 2  # AI move
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i, j] = 0  # Undo move
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:  # Alpha-Beta Pruning
                        break
        return best_score
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board[i, j] = 1  # Human move
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i, j] = 0  # Undo move
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:  # Alpha-Beta Pruning
                        break
        return best_score

# AI Move using Minimax
def ai_move():
    if st.session_state.difficulty == "Easy":
        # Random Move
        empty_cells = np.argwhere(st.session_state.board == 0)
        if empty_cells.size > 0:
            move = empty_cells[np.random.choice(len(empty_cells))]
            st.session_state.board[move[0], move[1]] = 2
            return

    elif st.session_state.difficulty == "Medium":
        # 50% Random, 50% Minimax
        if np.random.rand() < 0.5:
            empty_cells = np.argwhere(st.session_state.board == 0)
            if empty_cells.size > 0:
                move = empty_cells[np.random.choice(len(empty_cells))]
                st.session_state.board[move[0], move[1]] = 2
                return

    # Hard Mode (Full Minimax)
    best_score = -np.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i, j] == 0:
                st.session_state.board[i, j] = 2
                score = minimax(st.session_state.board, 0, False)
                st.session_state.board[i, j] = 0  # Undo move
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        st.session_state.board[best_move[0], best_move[1]] = 2

# Human Move
def make_move(row, col):
    if st.session_state.board[row, col] == 0 and st.session_state.winner is None:
        st.session_state.board[row, col] = 1
        winner = check_win(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            ai_move()
            winner = check_win(st.session_state.board)
            if winner:
                st.session_state.winner = winner

# Reset Game
def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.player = 1
    st.session_state.winner = None

# GUI Design
st.sidebar.markdown("### Difficulty Level")
st.session_state.difficulty = st.sidebar.radio("Select difficulty:", ["Easy", "Medium", "Hard"])

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>TIC TAC TOE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Test Your Skills Against AI! 🧠</h3>", unsafe_allow_html=True)

# Display Tic-Tac-Toe board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        with cols[j]:
            if st.session_state.board[i, j] == 0:
                st.button(" ", key=f"{i}-{j}", on_click=make_move, args=(i, j))
            elif st.session_state.board[i, j] == 1:
                st.button("❌", key=f"{i}-{j}", disabled=True)
            else:
                st.button("⭕", key=f"{i}-{j}", disabled=True)

# Display Winner or Draw
if st.session_state.winner is not None:
    if st.session_state.winner == 1:
        st.markdown("<h2 style='text-align: center; color: #58a6ff;'>You Win! 🎉</h2>", unsafe_allow_html=True)
    elif st.session_state.winner == 2:
        st.markdown("<h2 style='text-align: center; color: red;'>AI Wins! 🤖</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: white;'>It's a Draw! 😐</h2>", unsafe_allow_html=True)

# Reset Button
st.button("Reset Game", on_click=reset_game)

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #21262d;
        color: white;
        border: 2px solid #58a6ff;
        font-size: 24px;
        width: 100%;
        height: 100px;
    }
    .stButton button:disabled {
        background-color: #58a6ff;
        color: black;
        border: 2px solid #1f2937;
    }
    </style>
""", unsafe_allow_html=True)
