from bangtal import *
from enum import Enum

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

scene = Scene("Othello", "Images/background.png")

class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3

class Turn(Enum):
    BLACK = 2
    WHITE = 3
turn = Turn.BLACK

class Color(Enum):
    BLACK = 0
    WHITE = 1

class Score():
    def __init__(self, color):
        self.add_x = 0
        if color == Color.WHITE:
            self.add_x += 320

        self.digit_2 = Object("Images/0.png")
        self.digit_2.locate(scene, 770 + self.add_x, 250)
        self.digit_2.setScale(3)
        self.digit_2.hide()
        self.digit_1 = Object("Images/0.png")
        self.digit_1.setScale(3)
        self.digit_1.locate(scene, 830 + self.add_x, 250)
        self.digit_1.show()

    def setScore(self, num):
        if num // 10 > 0:
            self.digit_2.show()
            self.digit_2.setImage("Images/" + str(num//10) + ".png")
        self.digit_1.setImage("Images/" + str(num%10) + ".png")


def setState(x, y, s):
    object = board[y][x]
    object.state = s
    if s == State.BLANK:
        object.setImage("Images/blank.png")
    elif s == State.BLACK:
        object.setImage("Images/black.png")
    elif s == State.WHITE:
        object.setImage("Images/white.png")
    elif turn == Turn.BLACK:
        object.setImage("Images/black possible.png")
    else:
        object.setImage("Images/white possible.png")

def stone_onMouseAction(x, y):
    global turn
    global count_black
    global count_white

    object = board[y][x]
    if object.state == State.POSSIBLE:
        if turn == Turn.BLACK:
            setState(x, y, State.BLACK)
            reverse_xy(x, y)
            count_black += 1
            turn = Turn.WHITE
        else:
            setState(x, y, State.WHITE)
            reverse_xy(x, y)
            count_white += 1
            turn = Turn.BLACK

    score_black.setScore(count_black)
    score_white.setScore(count_white)

    if not setPossible():
        if turn == Turn.BLACK: turn = Turn.WHITE
        else: turn == Turn.BLACK

        if not setPossible():
            if count_black > count_white:
                showMessage("게임이 종료되었습니다.\n흑의 승리!")
            elif count_black < count_white:
                showMessage("게임이 종료되었습니다.\n백의 승리!")
            else:
                showMessage("게임이 종료되었습니다.\n무승부!")

    action_AI()

def setPossible_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False
    while True:
        x = x + dx
        y = y + dy

        if x < 0 or x > 7: return False
        if y < 0 or y > 7: return False
        
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            return possible
        else: return False

def setPossible_xy(x, y):
    object = board[y][x]
    if object.state == State.BLACK:return False
    if object.state == State.WHITE: return False
    setState(x, y, State.BLANK)

    if(setPossible_xy_dir(x, y, 0, 1)): return True
    if(setPossible_xy_dir(x, y, 1, 1)): return True
    if(setPossible_xy_dir(x, y, 1, 0)): return True
    if(setPossible_xy_dir(x, y, 1, -1)): return True
    if(setPossible_xy_dir(x, y, 0, -1)): return True
    if(setPossible_xy_dir(x, y, -1, -1)): return True
    if(setPossible_xy_dir(x, y, -1, 0)): return True
    if(setPossible_xy_dir(x, y, -1, 1)): return True
    return False

def reverse_xy_dir(x, y, dx, dy):
    global count_black
    global count_white
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False
    count = 0

    while True:
        x = x + dx
        y = y + dy

        if x < 0 or x > 7: return count
        if y < 0 or y > 7: return count
        
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy
                    object = board[y][x]
                    if object.state == other:
                        setState(x, y, mine)
                        if turn == Turn.BLACK:
                            count_black += 1
                            count_white -= 1
                        else:
                            count_black -= 1
                            count_white += 1
                        count += 1
                    else: return count

        else: return count


def reverse_xy(x, y):
    count = 0
    count += reverse_xy_dir(x, y, 0, 1)
    count += reverse_xy_dir(x, y, 1, 1)
    count += reverse_xy_dir(x, y, 1, 0)
    count += reverse_xy_dir(x, y, 1, -1)
    count += reverse_xy_dir(x, y, 0, -1)
    count += reverse_xy_dir(x, y, -1, -1)
    count += reverse_xy_dir(x, y, -1, 0)
    count += reverse_xy_dir(x, y, -1, 1)
    #print("count: ", count)


def action_AI():
    global turn
    global count_black
    global count_white

    if turn == Turn.BLACK:
        return

    pos_pos = get_possible_pos()
    count_index = []
    print("get_possible_pos: ", pos_pos)

    for pos_y, pos_x in pos_pos:
        count = 0
        count += count_possible(pos_x, pos_y, 0, 1)
        count += count_possible(pos_x, pos_y, 1, 1)
        count += count_possible(pos_x, pos_y, 1, 0)
        count += count_possible(pos_x, pos_y, 1, -1)
        count += count_possible(pos_x, pos_y, 0, -1)
        count += count_possible(pos_x, pos_y, -1, -1)
        count += count_possible(pos_x, pos_y, -1, 0)
        count += count_possible(pos_x, pos_y, -1, 1)
        count_index.append(count)
    
    max_count = max(count_index)
    index_max = count_index.index(max_count)
    
    setState(pos_x, pos_y, State.WHITE)
    reverse_xy(pos_pos[index_max][1], pos_pos[index_max][0])

    count_white += 1
    turn = Turn.BLACK

    score_black.setScore(count_black)
    score_white.setScore(count_white)

    if not setPossible():
        if turn == Turn.BLACK: turn = Turn.WHITE
        else: turn == Turn.BLACK

        if not setPossible():
            if count_black > count_white:
                showMessage("게임이 종료되었습니다.\n흑의 승리!")
            elif count_black < count_white:
                showMessage("게임이 종료되었습니다.\n백의 승리!")
            else:
                showMessage("게임이 종료되었습니다.\n무승부!")
    


def get_possible_pos():
    object = board
    pos_possible = []

    for y in range(8):
        for x in range(8):
            if object[y][x].state == State.POSSIBLE:
                pos_possible.append([y, x])
    return pos_possible

def count_possible(x, y, dx, dy):
    mine = State.WHITE
    other = State.BLACK

    possible = False
    count = 0

    while True:
        x = x + dx
        y = y + dy

        if x < 0 or x > 7: return count
        if y < 0 or y > 7: return count
        
        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy
                    object = board[y][x]
                    if object.state == other:
                        count += 1
                    else: return count

        else: return count

def setPossible():
    possible = False
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                setState(x, y, State.POSSIBLE)
                possible = True
    return possible

board = []
count_black = 0
count_white = 0

for y in range(8):
    board.append([])
    for x in range(8):
        object = Object("Images/blank.png")
        object.locate(scene, 40 + x * 80, 40 + y * 80)
        object.show()
        object.onMouseAction = lambda mx, my, action, ix = x, iy = y: stone_onMouseAction(ix, iy)
        object.state = State.BLANK

        board[y].append(object)

        
score_black = Score(Color.BLACK)
score_white = Score(Color.WHITE)

setState(3, 3, State.BLACK)
setState(4, 4, State.BLACK)
setState(3, 4, State.WHITE)
setState(4, 3, State.WHITE)
count_black += 2
count_white += 2
score_black.setScore(2)
score_white.setScore(2)

setPossible()

startGame(scene)