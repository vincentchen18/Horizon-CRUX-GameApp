import random
def empty_board():
    return [[0] * 4]*4

def spawn_tile(board):
    empty_indices = []
    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                empty_indices.append((x, y))
    spawntile = random.choice(empty_indices)
    if random.randint(1,10) == 10:
        board[spawntile[0]][spawntile[1]] = 4
    else:
        board[spawntile[0]][spawntile[1]] = 2
    return board

