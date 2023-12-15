import pprint

from flask import Flask, request
import copy

app = Flask(__name__)


def moves(board, pturn):
    mooves = []

    for row in range(len(board)):
        for column in range(len(board[row])):
            piece = board[row][column]
            tile = (row, column)
            #
            # if piece == "1r":
            #     if board[row - 1][column - 1] == "  " and column != 0:
            #         board[row - 1][column - 1], board[row][column] = board[row][column], board[row - 1][column - 1]
            #         board1 = copy.deepcopy(board)
            #         moves.append(board1)
            #         board[row - 1][column - 1], board[row][column] = board[row][column], board[row - 1][column - 1]
            #
            #     if board[row - 1][column + 1] == "  " and column != 0:
            #         board[row - 1][column + 1], board[row][column] = board[row][column], board[row - 1][column + 1]
            #         board1 = copy.deepcopy(board)
            #         moves.append(board1)
            #         board[row - 1][column + 1], board[row][column] = board[row][column], board[row - 1][column + 1]
            if piece == '  ':
                continue
            if pturn and '2' in piece:
                continue
            if not pturn and '1' in piece:
                continue
            directions = [
                (-1, -1),  # up, left
                (-1, 1),  # up, right
                (1, -1),  # down, left
                (1, 1)  # down, right
            ]

            for direction in directions:
                if direction[1] == -1:
                    if tile[1] == 0:
                        continue
                else:
                    if tile[1] == len(board[row]) - 1:
                        continue
                potential = (tile[0] + direction[0], tile[1] + direction[1])
                if direction[0] < 0:
                    if tile[0] == 0:
                        continue
                    if '1' in piece or 'u' in piece:
                        if board[potential[0]][potential[1]] == '  ':
                            board[tile[0]][tile[1]], board[potential[0]][potential[1]] = board[potential[0]][potential[1]], board[tile[0]][tile[1]]
                            mooves.append(copy.deepcopy(board))
                            board[tile[0]][tile[1]], board[potential[0]][potential[1]] = board[potential[0]][potential[1]], board[tile[0]][tile[1]]
                        elif board[tile[0]][tile[1]][0] == board[potential[0]][potential[1]][0]:
                            continue
                        else:
                            nextp = (potential[0] + direction[0], potential[1] + direction[1])
                            if 0 <= nextp[0] <= len(board) - 1 and 0 <= nextp[1] <= len(board[row]) - 1:
                                if board[nextp[0]][nextp[1]] == '  ':
                                    board[nextp[0]][nextp[1]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], board[nextp[0]][nextp[1]]
                                    newboard = copy.deepcopy(board)
                                    newboard[potential[0]][potential[1]] = '  '
                                    mooves.append(newboard)
                                    board[nextp[0]][nextp[1]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], board[nextp[0]][nextp[1]]

                else:
                    if tile[0] == len(board) - 1:
                        continue
                    if '2' in piece or 'u' in piece:
                        if board[potential[0]][potential[1]] == '  ':
                            board[tile[0]][tile[1]], board[potential[0]][potential[1]] = board[potential[0]][
                                potential[1]], board[tile[0]][tile[1]]
                            mooves.append(copy.deepcopy(board))
                            board[tile[0]][tile[1]], board[potential[0]][potential[1]] = board[potential[0]][
                                potential[1]], board[tile[0]][tile[1]]
                        elif board[tile[0]][tile[1]][0] == board[potential[0]][potential[1]][0]:
                            continue
                        else:
                            nextp = (potential[0] + direction[0], potential[1] + direction[1])
                            if 0 <= nextp[0] <= len(board) - 1 and 0 <= nextp[1] <= len(board[row]) - 1:
                                if board[nextp[0]][nextp[1]] == '  ':
                                    board[nextp[0]][nextp[1]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], \
                                    board[nextp[0]][nextp[1]]
                                    newboard = copy.deepcopy(board)
                                    newboard[potential[0]][potential[1]] = '  '
                                    mooves.append(newboard)
                                    board[nextp[0]][nextp[1]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], \
                                    board[nextp[0]][nextp[1]]

    return mooves


def minimax(board):
    score = winner(board)

    if score != 0:
        return score, board

    best = (1e9, None)

    for move in moves(board):
        score = maximin(move)

        if score < best[0]:
            best = (score, move)

    return best


def maximin(board):
    return "hhhhhhhhhh"


def winner(board):
    count1 = 0
    count2 = 0

    for row in board:
        for item in row:
            if "1" in item:
                count1 += 1
            elif "2" in item:
                count2 += 1

    if count1 == 0:
        return count2 * -100
    elif count2 == 0:
        return count1 * 100

    return 0


@app.route("/")
def hello():
    return "hello"


@app.route("/ai1", methods=["POST"])
def ai1():
    body = request.get_json()
    board = body["board"]

    # print("\n"*5)

    # for move in moves(board, False):
        # pprint.pprint(move)

    for row in range(len(board)):
        for column in range(len(board[row])):
            if "2" in board[row][column]:
                try:
                    if board[row + 1][column - 1] == "  " and column != 0:
                        board[row + 1][column - 1], board[row][column] = board[row][column], board[row + 1][column - 1]
                        return {"board": board}
                except Exception:
                    pass
                try:
                    if board[row + 1][column + 1] == "  " and column != len(board[row]) - 1:
                        board[row + 1][column + 1], board[row][column] = board[row][column], board[row + 1][column + 1]
                        return {"board": board}
                except Exception:
                    pass

    return {"board": board}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    board = [
        ['2r', '  ', '2r', '  ', '2r', '  ', '2r', '  '],
        ['  ', '2r', '  ', '2r', '  ', '2r', '  ', '2r'],
        ['2r', '  ', '2r', '  ', '2r', '  ', '2r', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '1r', '  ', '1r', '  ', '1r', '  ', '1r'],
        ['1r', '  ', '1r', '  ', '1r', '  ', '1r', '  '],
        ['  ', '1r', '  ', '1r', '  ', '1r', '  ', '1r']
    ]
