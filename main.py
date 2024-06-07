from PieceAndBoard import Piece, Board, ChessBoard
from ChessGameState import ChessGameState
import tkinter as tk

root = tk.Tk()

def parse_move(move_str):
    if len(move_str) == 6:  # 檢查是否是兩位數的起始和結束行號
        start_col, start_row, end_col, end_row = move_str[0], move_str[1:3], move_str[3], move_str[4:6]
    elif len(move_str) == 5:
        if move_str[1].isdigit() and move_str[2].isdigit():  # 檢查起始行號是否是兩位數
            start_col, start_row, end_col, end_row = move_str[0], move_str[1:3], move_str[3], move_str[4]
        else:  # 目標行號是兩位數
            start_col, start_row, end_col, end_row = move_str[0], move_str[1], move_str[2], move_str[3:5]
    else:  # 起始和目標行號都是一位數
        start_col, start_row, end_col, end_row = move_str[0], move_str[1], move_str[2], move_str[3]

    start_pos = (ord(start_col) - ord('a'), 10 - int(start_row))
    end_pos = (ord(end_col) - ord('a'), 10 - int(end_row))
    return start_pos, end_pos

def move_piece(board, start_pos, end_pos):
    piece = board.get_piece_at(start_pos)
    if piece:
        board.move_piece(piece, end_pos)
    else:
        raise ValueError("Invalid move: no piece at starting position.")

def is_valid_move(state, start_pos, end_pos):
    piece = state.board.get_piece_at(start_pos)
    if piece is None or piece.color != 'black':
        return False
    legal_moves = state.move_generator.get_legal_moves(piece)
    return end_pos in legal_moves

def ai_move():
    global current_state
    best_move = None
    best_value = float('-inf')
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)
        move_value = new_state.minimax(new_state, depth=3, alpha=float('-inf'), beta=float('inf'))
        if move_value > best_value:
            best_value = move_value
            best_move = move

    if best_move:
        current_state = current_state.make_move(best_move)
        piece, end_pos = best_move
        start_pos = piece.position
        move_str = f"{chr(start_pos[0] + ord('a'))}{10 - start_pos[1]}{chr(end_pos[0] + ord('a'))}{10 - end_pos[1]}"
        print(f"AI 移動: {move_str}")
        board_canvas.draw_pieces(current_state.board.pieces)
        current_state = ChessGameState(current_state.board, False)

    if current_state.is_terminal():
        print("遊戲結束，AI 贏了！")

def on_move():
    global current_state
    user_move = entry.get()
    try:
        start_pos, end_pos = parse_move(user_move)
        if not is_valid_move(current_state, start_pos, end_pos):
            raise ValueError("Invalid move: move is not allowed.")
        move_piece(current_state.board, start_pos, end_pos)
        print(f"玩家移動: {user_move}")
        board_canvas.draw_pieces(current_state.board.pieces)
        current_state = ChessGameState(current_state.board, True)
    except ValueError as e:
        print(e)
        return

    if current_state.is_terminal():
        print("遊戲結束，你贏了！")
        return

    # 呼叫 AI move
    root.after(100, ai_move)

def main():
    initial_pieces = [
        Piece('將', 'red', (4, 0)),
        Piece('士', 'red', (3, 0)),
        Piece('士', 'red', (5, 0)),
        Piece('車', 'red', (0, 0)),
        Piece('車', 'red', (8, 0)),
        Piece('馬', 'red', (7, 0)),
        Piece('馬', 'red', (1, 0)),
        Piece('相', 'red', (2, 0)),
        Piece('相', 'red', (6, 0)),
        Piece('炮', 'red', (1, 2)),
        Piece('炮', 'red', (7, 2)),
        Piece('兵', 'red', (0, 3)),
        Piece('兵', 'red', (2, 3)),
        Piece('兵', 'red', (4, 3)),
        Piece('兵', 'red', (6, 3)),
        Piece('兵', 'red', (8, 3)),
        Piece('帥', 'black', (4, 9)),
        Piece('仕', 'black', (3, 9)),
        Piece('仕', 'black', (5, 9)),
        Piece('車', 'black', (0, 9)),
        Piece('車', 'black', (8, 9)),
        Piece('馬', 'black', (7, 9)),
        Piece('馬', 'black', (1, 9)),
        Piece('象', 'black', (2, 9)),
        Piece('象', 'black', (6, 9)),
        Piece('炮', 'black', (1, 7)),
        Piece('炮', 'black', (7, 7)),
        Piece('卒', 'black', (0, 6)),
        Piece('卒', 'black', (2, 6)),
        Piece('卒', 'black', (4, 6)),
        Piece('卒', 'black', (6, 6)),
        Piece('卒', 'black', (8, 6))
    ]

    initial_board = Board(initial_pieces)
    global current_state
    current_state = ChessGameState(initial_board, True)

    root.title("Chinese Chess")

    global board_canvas, entry
    board_canvas = ChessBoard(root)
    board_canvas.pack()
    board_canvas.draw_pieces(initial_board.pieces)

    entry = tk.Entry(root)
    entry.pack()

    label = tk.Label(root, text="輸入你的移動（例如 e2e3）: ")
    label.pack()

    root.bind('<Return>', lambda event: on_move())

    root.mainloop()

if __name__ == "__main__":
    main()