class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.moves = 0
        self.winner = None
        self.winning_tokens = None
        self.players = ['X','O']
        self.current_player = 'X'

    def __repr__(self):
        board_str = ''
        for i, row in enumerate(self.board):
            display = row[:] # copy as we may modify
            if self.winning_tokens is not None: #(row, column tuples)
                for rindx, cindx in self.winning_tokens:
                    if rindx == i:
                        display[cindx] = f'\033[1;31m{row[cindx]}\033[0m' # convert to red
            board_str +='|'+'|'.join(display)+'|\n'
        return board_str
     
    def make_move(self, col):
        """Play the specified move and return True if the game is over."""
        if not self.is_valid_move(col):
            raise ValueError('Invalid move')
    
        self.current_player = self.players[self.moves%2]
        row = self.get_next_open_row(col)
        self.board[row][col] = self.current_player
        self.moves += 1

        if self.check_win(row, col, self.current_player):
            self.winner = self.current_player
            return True

        if self.is_board_full():
            self.winner = 'TIE'
            return True
        return False

    def valid_moves(self):
        return [c for c in range(self.cols) if self.is_valid_move(c)]

    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.board[0][col] == ' '

    def get_next_open_row(self, col):
        for row in range(self.rows-1, -1, -1): # backwards in 1 step increments
            if self.board[row][col] == ' ':
                return row
        return -1

    def is_board_full(self):
        return self.moves == self.rows * self.cols

    def check_win(self, row, col, player_token):
        #print('checking win for ',player_token)
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            #print(dr,dc)
            winning_tokens = [(row,col)]
            for step in range(1, 4):
                r, c = row + step*dr, col + step*dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player_token:
                    winning_tokens.append((r,c))
                else:
                    break
            for step in range(1, 4):
                r, c = row - step*dr, col - step*dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player_token:
                    winning_tokens.append((r,c))
                else:
                    break
            #print('winning:',winning_tokens)
            if len(winning_tokens) >= 4:
                self.winning_tokens = winning_tokens
                return True
        return False
