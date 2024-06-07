from MoveGenerator import MoveGenerator


class ChessGameState:
    def __init__(self, board, is_max_turn):
        self.board = board  # 棋盤狀態
        self.is_max_turn = is_max_turn  # 是否是最大化玩家的回合
        self.move_generator = MoveGenerator(board)

    def get_possible_moves(self):
        return self.move_generator.get_possible_moves(self.is_max_turn)

    def make_move(self, move):
        piece, end_pos = move
        new_board = self.board.copy()
        new_piece = new_board.get_piece_at(piece.position)
        new_board.move_piece(new_piece, end_pos)
        return ChessGameState(new_board, not self.is_max_turn)

    def is_terminal(self):
        red_general = any(piece.type == '將' for piece in self.board.pieces if piece.color == 'red')
        black_general = any(piece.type == '帥' for piece in self.board.pieces if piece.color == 'black')
        return not red_general or not black_general

    def evaluate(self):
        piece_values = {
            '將': 6000, '帥': 6000,
            '士': 120, '仕': 120,
            '象': 120, '相': 120,
            '馬': 280,
            '車': 700,
            '炮': 280,
            '兵': 30, '卒': 30
        }
        position_values = {
            # 其他棋子的類型也可以有類似的表
        }

        value = 0
        for piece in self.board.pieces:
            piece_value = piece_values.get(piece.type, 0)
            if piece.color == 'red':
                value += piece_value
            else:
                value -= piece_value
        return value

    def arc_consistency(self, state):
        for piece in state.board.pieces:
            legal_moves = state.move_generator.get_legal_moves(piece)
            if not legal_moves:
                piece.domain = []
            else:
                piece.domain = legal_moves

    def minimax(self, state, depth, alpha, beta):
        if depth == 0 or state.is_terminal():
            return state.evaluate()

        self.arc_consistency(state)  # 簡化問題

        if state.is_max_turn:
            max_eval = float('-inf')
            for move in state.get_possible_moves():
                eval = self.minimax(state.make_move(move), depth - 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta 剪枝
            return max_eval
        else:
            min_eval = float('inf')
            for move in state.get_possible_moves():
                eval = self.minimax(state.make_move(move), depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha 剪枝
            return min_eval
