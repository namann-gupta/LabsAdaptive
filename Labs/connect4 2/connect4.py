from player import HumanPlayer, RandomPlayer, MCTSPlayer
from board import Board
import copy

def play_game(player1, player2):
    """Run the game."""
    board = Board()
    players = [player1, player2]

    player_indx = 0
    game_ended = False
    while not game_ended:
        # display board
        print(board)

        # current player moves
        current_player = players[player_indx]
        selected_move = current_player.play(copy.deepcopy(board))
        print(f'Player {player_indx+1} played in column {selected_move}')
        game_ended = board.make_move(selected_move)
        
        # switch players
        player_indx = (player_indx + 1)%2
    
    # display final state of the board
    print(board)
    print(f'Game over. The winner is: {board.winner}')
    return board.winner
        
if __name__ == "__main__":
    player1 =  MCTSPlayer(max_time=2)
    player2 = MCTSPlayer(max_time=5)
    result = play_game(player1, player2)
    



