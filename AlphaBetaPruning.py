class node:      
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.child = []
        self.result = 0  
board = [[0, 0, 0] for i in range(3)]
# 0 代表空格
# 1 代表黑棋
# 2 代表白棋

# return 0: no one win and not finish
# return 1: finish and black win
# return 2: finish and white win
# return 3: finish and draw
def win():
    line = []
    for i in range(3): #3條直線跟橫線的座標
        line.append(((0,i), (1,i), (2,i)))
        line.append(((i,0), (i,1), (i,2)))
    line.append(((0,0), (1,1), (2,2))) #斜線座標
    line.append(((0,2), (1,1), (2,0)))
    for L in line:
        color = board[L[0][0]][L[0][1]] #直線上第一格是黑/白/空
        flag = True
        for grid in L:
            if board[grid[0]][grid[1]] == 0 or board[grid[0]][grid[1]] != color: #直線上有空格 or 有棋子顏色不同
                flag = False
                break
        if flag:
            return color
    ctr = 0
    for row in board:
        for x in row:
            if x != 0:
                ctr = ctr + 1
    if ctr == 9: #棋盤全部下完了 ->和局
        return 3
    return 0 #遊戲還沒結束 繼續進行中

#遞迴的樹搜索
def treeSearch(vertex, player, alpha, beta):
    value = win()
    if value != 0: # 葉節點 代表遊戲已結束
        #分數越高 對黑棋越有利
        if value == 1:
            vertex.result = 1
            return 1 #黑棋贏 返回分數1
        if value == 2:
            vertex.result = -1
            return -1 # 白棋贏 返回分數-1
        vertex.result = 0
        return 0 # 和局 返回分數0
    if player: # 換黑棋下 挑選子節點中 分數最高的
        value = -10000
        for x in range(3):
            for y in range(3):
                if board[x][y] == 0:  #空點 下下看
                    vertex.child.append(node(x, y))
                    board[x][y] = 1
                    value = max(value, treeSearch(vertex.child[-1], not player, alpha, beta))
                    alpha = max(alpha, value)
                    board[x][y] = 0
                    if alpha >= beta:
                        break
        vertex.result = value
        return value
    else: # 換白棋下 挑選子節點中 分數最低的
        value = 10000
        for x in range(3):
            for y in range(3):
                if board[x][y] == 0: #空點 下下看
                    vertex.child.append(node(x, y))
                    board[x][y] = 2
                    value = min(value, treeSearch(vertex.child[-1], not player, alpha, beta))
                    beta = min(beta, value)
                    board[x][y] = 0
                    if alpha >= beta:
                        break
        vertex.result = value
        return value

def drawBoard(): # 畫出棋盤根棋子
    for x in range(3):
        if x != 0:
            print('-+-+-')
        for y in range(3):
            if y != 0:
                print('|', end = '')
            if board[x][y] == 1:
                print('O', end = '')
            elif board[x][y] == 2:
                print('X', end = '')
            else:
                print(' ', end = '')
        print('')
def human():
    print('請輸入座標')
    x = input('')
    y = input('')
    return (int(x), int(y)) #return 人類玩家下的座標

def AI(player):
    root = node(-1,-1)
    val = treeSearch(root, player, -1e8, 1e8)
    # print(val)
    # print(root.result)
    print('AI可行下法與結果')
    for child in root.child:
        print(child.x, child.y, end = '\t')
        print(child.result)
    route = []
    vertex = root
    while len(vertex.child): # 找出雙方的最佳招法
        for v in vertex.child:
            if v.result == vertex.result:
                route.append((v.x, v.y))
                vertex = v
                break
    print('雙方最佳下法')
    for move in route:
        print(move)
    for v in root.child:
        if v.result == root.result:
            return (v.x, v.y) #return AI玩家下的座標
def main():
    print('玩家先下按 O\nAI先下按 X\n')
    first = input('')
    while first != 'O' and first != 'X' and first != 'o' and first != 'x':
        first = input('')
    AIplayer = first == 'X' or first == 'x'
    if not AIplayer:
        humanMove = human()
        if AIplayer:
            board[humanMove[0]][humanMove[1]] = 2
        else:
            board[humanMove[0]][humanMove[1]] = 1
        if win() != 0:
            if win() == 3:
                print('DRAW!!')
            else:
                print('HUMAN WIN!!')
            return
    while True:
        AImove = AI(AIplayer)
        print('AI 最後下在', AImove)
        print('')
        if AIplayer:
            board[AImove[0]][AImove[1]] = 1
        else:
            board[AImove[0]][AImove[1]] = 2
        if win() != 0:
            if win() == 3:
                print('DRAW!!')
            else:
                print('AI WIN!!')
            return
        drawBoard()
        humanMove = human()
        if AIplayer:
            board[humanMove[0]][humanMove[1]] = 2
        else:
            board[humanMove[0]][humanMove[1]] = 1
        if win() != 0:
            if win() == 3:
                print('DRAW!!')
            else:
                print('HUMAN WIN!!')
            return

main()