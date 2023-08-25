#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import chess_engine
import pygame as py

import ai_engine
from enums import Player
import logging

"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]
logging.basicConfig(filename='chess.log',
                    level=logging.INFO,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')


# TODO: AI black has been worked on. Mirror progress for other two modes
def load_images():
    """
    Load images for the chess pieces
    """
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    """ Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    """
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


def draw_squares(screen):
    """ Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    """ Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))


def main():
    # Check for the number of players and the color of the AI
    human_player = ""
    while True:
        try:
            number_of_players = input("How many players (1 or 2)?\n")
            if int(number_of_players) == 1:
                number_of_players = 1
                while True:
                    human_player = input("What color do you want to play (w or b)?\n")
                    if human_player == "w" or human_player == "b":
                        break
                    else:
                        print("Enter w or b.\n")
                break
            elif int(number_of_players) == 2:
                number_of_players = 2
                break
            else:
                print("Enter 1 or 2.\n")
        except ValueError:
            print("Enter 1 or 2.")

    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    # game_state = chess_engine.game_state()
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False

    ai = ai_engine.chess_ai()
    game_state = chess_engine.game_state()
    if human_player == 'b':
        logging.info("The AI player starts.")
        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
        game_state.move_piece(ai_move[0], ai_move[1], True)
    else:
        logging.info("The human player starts.")

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        # this if is useless right now
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                        else:
                            game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                  (player_clicks[1][0], player_clicks[1][1]), False)
                            draw_game_state(screen, game_state, valid_moves, square_selected)
                            py.display.update()
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []

                            if human_player == 'w':
                                ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                                game_state.move_piece(ai_move[0], ai_move[1], True)
                            elif human_player == 'b':
                                ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
                                game_state.move_piece(ai_move[0], ai_move[1], True)
                    else:
                        valid_moves = game_state.get_valid_moves((row, col))
                        if valid_moves is None:
                            valid_moves = []
            elif e.type == py.KEYDOWN:
                if e.key == py.K_r:
                    game_over = False
                    game_state = chess_engine.game_state()
                    valid_moves = []
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                elif e.key == py.K_u:
                    game_state.undo_move()
                    print(len(game_state.move_log))

        draw_game_state(screen, game_state, valid_moves, square_selected)

        endgame = game_state.checkmate_stalemate_checker()
        if endgame in range(3):
            if endgame == 0:
                game_over = True
                draw_text(screen, "Black wins.")
                logging.info("The game ends with Black's winning.")
            elif endgame == 1:
                game_over = True
                draw_text(screen, "White wins.")
                logging.info("The game ends with White's winning.")
            elif endgame == 2:
                game_over = True
                draw_text(screen, "Stalemate.")
                logging.info("The game ends in a stalemate.")

            running = False

            py.display.update()
            py.time.wait(2000)

            # logs
            white_check_counter = sum(1 for i in range(0, len(game_state.move_log), 2) if game_state.move_log[i].in_check)
            black_check_counter = sum(1 for i in range(1, len(game_state.move_log), 2) if game_state.move_log[i].in_check)
            logging.info(f"Number of white chess: {white_check_counter}.")
            logging.info(f"Number of black chess: {black_check_counter}.")

            len_move_log = len(game_state.move_log)
            all_white_tools_survived = all_black_tools_survived = len_move_log
            for i in range(len_move_log):
                try:
                    if game_state.move_log[i].removed_piece.get_player() == Player.PLAYER_1:
                        if all_white_tools_survived == len_move_log:  # if not changed yet
                            all_white_tools_survived = i
                    elif game_state.move_log[i].removed_piece.get_player() == Player.PLAYER_2:
                        if all_black_tools_survived == len_move_log:  # if not changed yet
                            all_black_tools_survived = i
                except AttributeError:
                    pass
                if all_black_tools_survived != len_move_log and all_white_tools_survived != len_move_log:
                    break

            logging.info(f"All white tools survived {all_white_tools_survived} out of {len_move_log} turns.")
            logging.info(f"All black tools survived {all_black_tools_survived} out of {len_move_log} turns.")

            knight_moves = [1 if move.moving_piece.get_name() == 'n' else 0 for move in game_state.move_log]
            white_knight_moves = sum(knight_moves[0::2])
            black_knight_moves = sum(knight_moves[1::2])
            logging.info(f"Number of white knight moves: {white_knight_moves}.")
            logging.info(f"Number of black knight moves: {black_knight_moves}.\n\t\t----------END GAME----------\n\n")

        clock.tick(MAX_FPS)
        py.display.flip()


def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Black"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()
