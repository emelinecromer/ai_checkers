import pprint

from flask import Flask, request
import copy

app = Flask(__name__)


def moves(board, pturn):
    global t
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

            else:
                if tile[0] == len(board) - 1:
                    continue
                if '2' in piece or 'u' in piece:
                    if board[potential[0]][potential[1]] == '  ':
                        board[tile[0]][tile[1]], board[potential[0]][potential[1]] = board[potential[0]][
                            potential[1]], board[tile[0]][tile[1]]
                        newboard = copy.deepcopy(board)
                        if potential[0] == len(newboard) - 1:
                            newboard[potential[0]][potential[1]] = "2u"
                        mooves.append(newboard)
                        board[tile[0]][tile[1]], board[potential[0]][potential[1]] = board[potential[0]][
                            potential[1]], board[tile[0]][tile[1]]
                    elif board[tile[0]][tile[1]][0] == board[potential[0]][potential[1]][0]:
                        continue
                    else:
                        nextp = (potential[0] + direction[0], potential[1] + direction[1])
                        if 0 <= nextp[0] <= len(board) - 1 and 0 <= nextp[1] <= len(board[row]) - 1:
                            board[nextp[0]][nextp[1]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], \
                                board[nextp[0]][nextp[1]]
                            newboard = copy.deepcopy(board)
                            newboard[potential[0]][potential[1]] = '  '
                            if nextp[0] == len(board) - 1:
                                newboard[nextp[0]][nextp[1]] = "2u"
                            mooves.append(newboard)
                            board[nextp[0]][nextp[1]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], \
                                board[nextp[0]][nextp[1]]

    return mooves


def minimax(board, depth, maxdepth):
    score = winner(board)

    # check if the absolute value of the score is >= 100 or depth is greater than max depth if true return score, board
    # otherwise continue with the line that says best= and the for loop

    if depth > maxdepth or abs(score) >= 100:
        return score, board

    best = (1e9, None)

    for move in moves(board, False):
        score, b = maximin(move, depth=depth + 1, maxdepth=maxdepth)

        if score < best[0]:
            best = (score, move)

    return best


def maximin(board, depth, maxdepth):
    score = winner(board)

    if depth > maxdepth or abs(score) >= 100:
        return score, board

    best = (-1e9, None)

    for move in moves(board, True):
        score, b = minimax(move, depth=depth + 1, maxdepth=maxdepth)

        if score > best[0]:
            best = (score, move)

    return best


def winner(board):
    count1 = 0
    count2 = 0

    for row in board:
        for item in row:
            if "1" in item:
                count1 += 1
                if "u" in item:
                    count1 += 1
            elif "2" in item:
                count2 += 1
                if "u" in item:
                    count2 += 1

    if count1 == 0:
        return count2 * -100
    elif count2 == 0:
        return count1 * 100

    return count1 - count2


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

    # todo try new minimax ai

    return {"board": board}


@app.route("/ai2", methods=["POST"])
def ai2():
    body = request.get_json()
    board = body["board"]
    score, new_board = minimax(board, depth=0, maxdepth=3)
    return {"board": new_board}


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
