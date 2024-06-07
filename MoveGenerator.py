class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def get_possible_moves(self, is_max_turn):
        possible_moves = []
        for piece in self.board.pieces:
            if (is_max_turn and piece.color == 'red') or (not is_max_turn and piece.color == 'black'):
                moves = self.get_legal_moves(piece)
                for move in moves:
                    possible_moves.append((piece, move))
        return possible_moves

    def get_legal_moves(self, piece):
        if piece.type == '將' or piece.type == '帥':
            return self.get_general_moves(piece)
        elif piece.type == '士' or piece.type == '仕':
            return self.get_advisor_moves(piece)
        elif piece.type == '象' or piece.type == '相':
            return self.get_elephant_moves(piece)
        elif piece.type == '馬':
            return self.get_horse_moves(piece)
        elif piece.type == '車':
            return self.get_rook_moves(piece)
        elif piece.type == '炮':
            return self.get_cannon_moves(piece)
        elif piece.type == '兵' or piece.type == '卒':
            return self.get_pawn_moves(piece)
        return []

    # 將軍的移動限制
    def get_general_moves(self, piece):
        moves = []
        x, y = piece.position
        possible_positions = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
        for pos in possible_positions:
            if self.is_within_palace_general(piece, pos) and not self.is_occupied_by_same_side(piece, pos):
                moves.append(pos)
        return moves

    # 士的移動限制
    def get_advisor_moves(self, piece):
        moves = []
        x, y = piece.position
        possible_positions = [(x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        for pos in possible_positions:
            if self.is_within_palace_general(piece, pos) and not self.is_occupied_by_same_side(piece, pos):
                moves.append(pos)
        return moves

    # 象的移動限制
    def get_elephant_moves(self, piece):
        moves = []
        x, y = piece.position
        possible_positions = [(x+2, y+2), (x-2, y-2), (x+2, y-2), (x-2, y+2)]
        for pos in possible_positions:
            if self.is_within_palace_elephant(piece, pos) and not self.is_occupied_by_same_side(piece, pos):
                moves.append(pos)
        return moves

    # 馬的移動限制
    def get_horse_moves(self, piece):
        moves = []
        x, y = piece.position
        knight_moves = [
            ((x + 2, y + 1), (x + 1, y)),
            ((x + 2, y - 1), (x + 1, y)),
            ((x - 2, y + 1), (x - 1, y)),
            ((x - 2, y - 1), (x - 1, y)),
            ((x + 1, y + 2), (x, y + 1)),
            ((x - 1, y + 2), (x, y + 1)),
            ((x + 1, y - 2), (x, y - 1)),
            ((x - 1, y - 2), (x, y - 1))
        ]

        for move, block in knight_moves:
            if self.is_within_bounds(move) and not self.is_occupied_by_same_side(piece, move) and not self.is_blocked(
                    block):
                moves.append(move)

        return moves

    # 車的移動限制
    def get_rook_moves(self, piece):
        moves = []
        x, y = piece.position

        # 向上移動
        for i in range(y + 1, 10):
            if not self.add_move_if_possible(piece, (x, i), moves):
                break

        # 向下移動
        for i in range(y - 1, -1, -1):
            if not self.add_move_if_possible(piece, (x, i), moves):
                break

        # 向右移動
        for i in range(x + 1, 9):
            if not self.add_move_if_possible(piece, (i, y), moves):
                break

        # 向左移動
        for i in range(x - 1, -1, -1):
            if not self.add_move_if_possible(piece, (i, y), moves):
                break

        return moves

    # 炮的移動限制
    def get_cannon_moves(self, piece):
        moves = []
        x, y = piece.position

        # 向上移動
        self.add_cannon_moves(piece, x, y, 0, 1, moves)
        # 向下移動
        self.add_cannon_moves(piece, x, y, 0, -1, moves)
        # 向右移動
        self.add_cannon_moves(piece, x, y, 1, 0, moves)
        # 向左移動
        self.add_cannon_moves(piece, x, y, -1, 0, moves)

        return moves

    # 偵測炮可以跳到哪裡（攻擊）or 單純移動
    def add_cannon_moves(self, piece, x, y, dx, dy, moves):
        jumped = False
        for i in range(1, 10):
            new_x = x + dx * i
            new_y = y + dy * i
            if not self.is_within_bounds((new_x, new_y)):
                break
            target_piece = self.board.get_piece_at((new_x, new_y))
            if not jumped:
                if target_piece is None:
                    moves.append((new_x, new_y))
                else:
                    jumped = True
            else:
                if target_piece is None:
                    continue
                elif target_piece.color != piece.color:
                    moves.append((new_x, new_y))
                    break
                else:
                    break

    # 兵的移動限制
    def get_pawn_moves(self, piece):
        moves = []
        x, y = piece.position
        if piece.color == 'red':
            if y < 9:  # 向前
                self.add_move_if_possible(piece, (x, y + 1), moves)
            if y >= 5:  # 過河後可以橫向
                self.add_move_if_possible(piece, (x + 1, y), moves)
                self.add_move_if_possible(piece, (x - 1, y), moves)
        else:
            if y > 0:  # 向前
                self.add_move_if_possible(piece, (x, y - 1), moves)
            if y <= 4:  # 過河後可以橫向
                self.add_move_if_possible(piece, (x + 1, y), moves)
                self.add_move_if_possible(piece, (x - 1, y), moves)

        return moves

    # 兵的移動工具
    def add_move_if_possible(self, piece, pos, moves):
        if self.is_within_bounds(pos):
            target_piece = self.board.get_piece_at(pos)
            if target_piece is None or target_piece.color != piece.color:
                moves.append(pos)
                return True
            return False
        return False

    # 將軍、士的移動區域
    def is_within_palace_general(self, piece, position):
        x, y = position
        if piece.color == 'red':
            return 3 <= x <= 5 and 0 <= y <= 2
        else:
            return 3 <= x <= 5 and 7 <= y <= 9

    # 象的移動區域
    def is_within_palace_elephant(self, piece, position):
        x, y = position
        if piece.color == 'red':
            return 0 <= x <= 8 and 0 <= y <= 4
        else:
            return 0 <= x <= 8 and 5 <= y <= 9

    # 用於直線移動棋子的路徑檢測
    def add_move_if_possible(self, piece, pos, moves):
        if self.is_within_bounds(pos):
            target_piece = self.board.get_piece_at(pos)
            if target_piece is None:
                moves.append(pos)
                return True
            elif target_piece.color != piece.color:
                moves.append(pos)
                return False
            else:
                return False
        return False

    # 大部分棋子的邊界限制
    def is_within_bounds(self, position):
        x, y = position
        return 0 <= x <= 8 and 0 <= y <= 9

    # 該位置有其他棋子
    def is_occupied_by_same_side(self, piece, position):
        target_piece = self.board.get_piece_at(position)
        return target_piece and target_piece.color == piece.color

    def is_blocked(self, position):
        return self.board.get_piece_at(position) is not None
