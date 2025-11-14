"""Simple, reliable Tic-Tac-Toe CLI game.

Features:
- Human vs Human
- Human vs Computer (unbeatable AI using Minimax)

Run:
	python main.py

The module also exposes functions used by tests: check_winner, best_move, available_moves, is_full.
"""

from typing import List, Optional, Tuple

WIN_COMBINATIONS = [
	(0, 1, 2),
	(3, 4, 5),
	(6, 7, 8),
	(0, 3, 6),
	(1, 4, 7),
	(2, 5, 8),
	(0, 4, 8),
	(2, 4, 6),
]


def new_board() -> List[str]:
	return [" "] * 9


def print_board(board: List[str], show_positions: bool = False) -> None:
	def cell(i):
		return board[i] if board[i] != " " or not show_positions else str(i + 1)

	rows = []
	for r in range(3):
		rows.append(" | ".join(cell(r * 3 + c) for c in range(3)))
	print("\n---------\n".join(rows))


def available_moves(board: List[str]) -> List[int]:
	return [i for i, v in enumerate(board) if v == " "]


def is_full(board: List[str]) -> bool:
	return all(cell != " " for cell in board)


def check_winner(board: List[str]) -> Optional[str]:
	for a, b, c in WIN_COMBINATIONS:
		if board[a] != " " and board[a] == board[b] == board[c]:
			return board[a]
	return None


def minimax(board: List[str], player: str) -> Tuple[int, Optional[int]]:
	# player is the current mover ('X' human or 'O' computer)
	winner = check_winner(board)
	if winner == "O":
		return (1, None)
	if winner == "X":
		return (-1, None)
	if is_full(board):
		return (0, None)

	moves = available_moves(board)
	if player == "O":
		best_score = -2
		best_move = None
		for m in moves:
			board[m] = "O"
			score, _ = minimax(board, "X")
			board[m] = " "
			if score > best_score:
				best_score = score
				best_move = m
		return best_score, best_move
	else:
		best_score = 2
		best_move = None
		for m in moves:
			board[m] = "X"
			score, _ = minimax(board, "O")
			board[m] = " "
			if score < best_score:
				best_score = score
				best_move = m
		return best_score, best_move


def best_move(board: List[str]) -> int:
	# returns index 0..8 for best computer move
	_, move = minimax(board, "O")
	if move is None:
		# fallback: choose first available
		moves = available_moves(board)
		return moves[0]
	return move


def player_move(board: List[str], symbol: str) -> None:
	while True:
		try:
			choice = input(f"Player {symbol}, enter position (1-9): ").strip()
			pos = int(choice) - 1
			if pos not in range(9):
				print("Invalid number. Pick 1-9.")
				continue
			if board[pos] != " ":
				print("That square is taken. Pick another.")
				continue
			board[pos] = symbol
			break
		except ValueError:
			print("Please enter a number 1-9.")


def computer_move(board: List[str]) -> None:
	m = best_move(board)
	board[m] = "O"


def play_game() -> None:
	print("Welcome to Tic-Tac-Toe")
	print("Choose mode:\n1) Player vs Computer\n2) Player vs Player")
	while True:
		mode = input("Mode (1 or 2): ").strip()
		if mode in ("1", "2"):
			break
		print("Enter 1 or 2.")

	board = new_board()
	current = "X"  # X always starts
	show_positions = True

	if mode == "1":
		# Human is X, Computer is O
		while True:
			print_board(board, show_positions=show_positions)
			show_positions = False
			if current == "X":
				player_move(board, "X")
			else:
				print("Computer is thinking...")
				computer_move(board)

			winner = check_winner(board)
			if winner or is_full(board):
				print_board(board)
				if winner:
					if winner == "X":
						print("You win! 🎉")
					else:
						print("Computer wins. Try again!")
				else:
					print("It's a tie.")
				break
			current = "O" if current == "X" else "X"

	else:
		# PvP
		while True:
			print_board(board, show_positions=show_positions)
			show_positions = False
			player_move(board, current)
			winner = check_winner(board)
			if winner or is_full(board):
				print_board(board)
				if winner:
					print(f"Player {winner} wins! 🎉")
				else:
					print("It's a tie.")
				break
			current = "O" if current == "X" else "X"


if __name__ == "__main__":
	play_game()

