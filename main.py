from pprint import pprint

import pygame
import requests

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("checkers")
clock = pygame.time.Clock()

player_turn = True

stage = "game"

tile = None

# board = [
#     ['2r', '  ', '2r', '  ', '2r', '  ', '2r', '  '],
#     ['  ', '2r', '  ', '2r', '  ', '2r', '  ', '2r'],
#     ['2r', '  ', '2r', '  ', '2r', '  ', '2r', '  '],
#     ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
#     ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
#     ['  ', '1r', '  ', '1r', '  ', '1r', '  ', '1r'],
#     ['1r', '  ', '1r', '  ', '1r', '  ', '1r', '  '],
#     ['  ', '1r', '  ', '1r', '  ', '1r', '  ', '1r']
# ]

board = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '1r', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '2u', '  ', '2r', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '1u', '  ', '1r', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
]

font = pygame.font.Font(None, 150)


def computer_turn():
    res = requests.post("http://localhost:5000/ai1", json={"board": board})
    new_board = res.json()["board"]

    for row in range(len(board)):
        board[row] = new_board[row]


while True:

    # events
    for event in pygame.event.get():
        if stage == "game":
            if player_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if pos[0] < 320 or pos[0] > 960 or pos[1] < 30 or pos[1] > 670:
                        continue

                    pos = list(pos)
                    pos[0] -= 320
                    pos[1] -= 30

                    pos[0] //= 80
                    pos[1] //= 80

                    # print(f"row {pos[1]}, column {pos[0]}")

                    if (pos[1], pos[0]) == tile:
                        tile = None

                    elif "2" in board[pos[1]][pos[0]]:
                        tile = None

                    elif tile is None:
                        tile = (pos[1], pos[0])

                    elif board[pos[1]][pos[0]] == '  ':
                        # move up
                        if pos[1] == tile[0] - 1:
                            if abs(pos[0] - tile[1]) == 1:
                                board[pos[1]][pos[0]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], board[pos[1]][
                                    pos[0]]
                                tile = None
                                player_turn = False

                        elif pos[1] == tile[0] - 2:
                            # move up and right by 2
                            if pos[0] - tile[1] == 2 and "2" in board[tile[0] - 1][tile[1] + 1]:
                                board[tile[0] - 1][tile[1] + 1] = '  '
                                board[pos[1]][pos[0]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], board[pos[1]][
                                    pos[0]]
                                tile = None
                                player_turn = False

                            # move up and left by 2
                            elif pos[0] - tile[1] == -2 and "2" in board[tile[0] - 1][tile[1] - 1]:
                                board[tile[0] - 1][tile[1] - 1] = '  '
                                board[pos[1]][pos[0]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], board[pos[1]][
                                    pos[0]]
                                tile = None
                                player_turn = False
                            else:
                                print("nuh uh theres no piece there to take")

                        elif "u" in board[tile[0]][tile[1]]:
                            # move down
                            if pos[1] == tile[0] + 1:
                                if abs(pos[0] - tile[1]) == 1:
                                    board[pos[1]][pos[0]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], \
                                    board[pos[1]][
                                        pos[0]]
                                    tile = None
                                    player_turn = False

                            elif pos[1] == tile[0] + 2:
                                # move down and right by 2
                                if pos[0] - tile[1] == 2 and "2" in board[tile[0] + 1][tile[1] + 1]:
                                    board[tile[0] + 1][tile[1] + 1] = '  '
                                    board[pos[1]][pos[0]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], \
                                    board[pos[1]][
                                        pos[0]]
                                    tile = None
                                    player_turn = False

                                # move down and left by 2
                                elif pos[0] - tile[1] == -2 and "2" in board[tile[0] + 1][tile[1] - 1]:
                                    board[tile[0] + 1][tile[1] - 1] = '  '
                                    board[pos[1]][pos[0]], board[tile[0]][tile[1]] = board[tile[0]][tile[1]], \
                                    board[pos[1]][
                                        pos[0]]
                                    tile = None
                                    player_turn = False

                        else:
                            print("nuh uh you cant go there")

                    else:
                        tile = (pos[1], pos[0])

                    count1 = 0
                    count2 = 0

                    for row in board:
                        for item in row:
                            if "1" in item:
                                count1 += 1
                            elif "2" in item:
                                count2 += 1

                    if count1 == 0:
                        stage = "p2 win"
                    elif count2 == 0:
                        stage = "p1 win"

        if event.type == pygame.QUIT:
            pygame.quit()

    # draw
    screen.fill((255, 255, 255))

    if stage == "game":
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(320, 30, 640, 640))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(318, 28, 644, 644), width=4)

        for i in range(0, 8):
            for j in range(0, 4):
                if i % 2 == 0:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(320 + 160 * j, 30 + 80 * i, 80, 80))
                    if board[i][2 * j][0] == "2":
                        if "u" in board[i][2 * j]:
                            pygame.draw.circle(screen, (255, 0, 120) if (i, 2 * j) != tile else (0, 0, 200),
                                               (360 + 160 * j, 70 + 80 * i), 30)
                        else:
                            pygame.draw.circle(screen, (255, 0, 0) if (i, 2 * j) != tile else (0, 0, 200),
                                               (360 + 160 * j, 70 + 80 * i), 30)
                    elif board[i][2 * j][0] == "1":
                        if "u" in board[i][2 * j]:
                            pygame.draw.circle(screen, (120, 0, 255) if (i, 2 * j) != tile else (0, 0, 200),
                                               (360 + 160 * j, 70 + 80 * i), 30)
                        else:
                            pygame.draw.circle(screen, (0, 0, 255) if (i, 2 * j) != tile else (0, 0, 200),
                                               (360 + 160 * j, 70 + 80 * i), 30)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(400 + 160 * j, 30 + 80 * i, 80, 80))
                    if board[i][2 * j + 1][0] == "2":
                        if "u" in board[i][2 * j + 1]:
                            pygame.draw.circle(screen, (255, 0, 120) if (i, 2 * j + 1) != tile else (200, 0, 0),
                                               (440 + 160 * j, 70 + 80 * i), 30)
                        else:
                            pygame.draw.circle(screen, (255, 0, 0) if (i, 2 * j + 1) != tile else (200, 0, 0),
                                               (440 + 160 * j, 70 + 80 * i), 30)
                    elif board[i][2 * j + 1][0] == "1":
                        if "u" in board[i][2 * j + 1]:
                            pygame.draw.circle(screen, (120, 0, 255) if (i, 2 * j + 1) != tile else (0, 0, 200),
                                               (440 + 160 * j, 70 + 80 * i), 30)
                        else:
                            pygame.draw.circle(screen, (0, 0, 255) if (i, 2 * j + 1) != tile else (0, 0, 200),
                                               (440 + 160 * j, 70 + 80 * i), 30)

    elif stage == "p1 win":
        text = font.render("you won yayyyy", True, (0, 0, 0))
        screen.blit(text, (1280 / 2 - text.get_width() / 2, 720 / 2 - text.get_height() / 2))

    elif stage == "p2 win":
        text = font.render("you lost uh oh", True, (0, 0, 0))
        screen.blit(text, (1280 / 2 - text.get_width() / 2, 720 / 2 - text.get_height() / 2))

    pygame.display.flip()
    clock.tick(60)

    if not player_turn:
        computer_turn()
        player_turn = True
