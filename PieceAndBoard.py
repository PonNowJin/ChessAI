import tkinter as tk

class Piece:
    def __init__(self, piece_type, color, position, displayColor):
        self.type = piece_type  # 棋子的類型（如：將、士、象、馬、車、炮、兵）
        self.color = color      # 棋子的顏色（紅方或黑方）
        self.position = position  # 棋子的位置（如：(0, 0) 表示在左上角）
        self.domain = []
        self.displayColor = displayColor

    def __repr__(self):
        return f"{self.color[0].upper()}{self.type[0].upper()}@{self.position}"

class Board:
    def __init__(self, pieces=None):
        if pieces is None:
            pieces = []
        self.pieces = pieces  # 所有棋子

    def get_piece_at(self, position):
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    # 移動棋子並更新位置
    def move_piece(self, piece, new_position):
        target_piece = self.get_piece_at(new_position)
        if target_piece and target_piece.color != piece.color:
            self.remove_piece(target_piece)
        piece.position = new_position

    # 從棋盤移除棋子
    def remove_piece(self, piece):
        self.pieces.remove(piece)

    # 返回棋盤的副本（深拷貝）
    def copy(self):
        new_pieces = [Piece(piece.type, piece.color, piece.position, piece.displayColor) for piece in self.pieces]
        return Board(new_pieces)

    def print_board(self):
        board_display = [[' ' for _ in range(9)] for _ in range(10)]
        for piece in self.pieces:
            x, y = piece.position
            board_display[y][x] = f"{piece.color[0].upper()}{piece.type[0].upper()}"
        print("  a b c d e f g h i")
        for i in range(10):
            print(f"{10 - i} {' '.join(board_display[i])}")

class ChessBoard(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=500, height=600)
        self.parent = parent
        self.create_grid()
        self.pieces = []

    def create_grid(self):
        for i in range(10):
            self.create_text(30, i * 50 + 25, text=str(10 - i), font=("Arial", 16))
        for i in range(10):
            for j in range(9):
                self.create_rectangle(j * 50 + 50, i * 50, (j + 1) * 50 + 50, (i + 1) * 50, outline="black")

        # 添加底部的英文字母列標記
        for j in range(9):
            self.create_text(j * 50 + 75, 510, text=chr(ord('a') + j), font=("Arial", 16))

    def draw_pieces(self, pieces):
        self.pieces = pieces
        self.delete("piece")
        for piece in pieces:
            x, y = piece.position
            color = "red" if piece.displayColor == "red" else "black"
            self.create_text(x * 50 + 75, y * 50 + 25, text=f"{piece.type[0].upper()}",
                             tags="piece", font=("Arial", 24), fill=color)
