from ast import While
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_POINTS_COUNT = 4

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) #size of board (height, width)
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col]==0:
            return i

def print_board(board):
    print(np.flip(board,0))

def winning_move(board, row, col):
    contador = 1
    #verifica verticalmente
    seq_vertical = 1
    end_up = False
    while (not end_up) and row+contador<ROW_COUNT:
        if board[row][col]==board[row+contador][col]:
            seq_vertical+=1
            contador+=1
        else:
            end_up=True
    end_down = False
    contador = 1
    while (not end_down) and row-contador>=0:
        if board[row][col]==board[row-contador][col]:
            seq_vertical+=1
            contador+=1
        else:
            end_down=True
    if seq_vertical>=WIN_POINTS_COUNT:
        return True    
    contador = 1

    #verifica horizontalmente
    seq_horizontal = 1
    end_right = False
    while (not end_right) and col+contador<COLUMN_COUNT:
        if board[row][col]==board[row][col+contador]:
            seq_horizontal+=1
            contador+=1
        else:
            end_right=True
    end_left = False
    contador = 1
    while (not end_left) and col-contador>=0:
        if board[row][col]==board[row][col-contador]:
            seq_horizontal+=1
            contador+=1
        else:
            end_left=True
    if seq_horizontal>=WIN_POINTS_COUNT:
        return True
    contador = 1

    #verifica diagonal ascendente direita
    seq_diag_right = 1
    end_up_right = False
    while (not end_up_right) and col+contador<COLUMN_COUNT and row+contador<ROW_COUNT:
        if board[row][col]==board[row+contador][col+contador]:
            seq_diag_right+=1
            contador+=1
        else:
            end_up_right=True
    contador = 1
    end_down_left = False
    while (not end_down_left) and col-contador>=0 and row-contador>=0:
        if board[row][col]==board[row-contador][col-contador]:
            seq_diag_right+=1
            contador+=1
        else:
            end_down_left=True
    if seq_diag_right>=WIN_POINTS_COUNT:
        return True
    contador = 1

    #verifica diagonal ascendente esquerda
    seq_diag_left = 1
    end_up_left = False
    while (not end_up_left) and col-contador>=0 and row+contador<ROW_COUNT:
        if board[row][col]==board[row+contador][col-contador]:
            seq_diag_left+=1
            contador+=1
        else:
            end_up_left=True
    contador = 1
    end_down_right = False
    while (not end_down_right) and col+contador<COLUMN_COUNT and row-contador>=0:
        if board[row][col]==board[row-contador][col+contador]:
            seq_diag_left+=1
            contador+=1
        else:
            end_down_right=True
    if seq_diag_right>=WIN_POINTS_COUNT:
        return True
    return False

board = create_board()
game_over = False
turn = 0

while not game_over:
    if turn==0:
        numero = False
        while not numero:
            col = input("Jogador 1 faz a jogada (0-"+str(COLUMN_COUNT-1)+"): ")
            try:
                col = int(col)
                if col<COLUMN_COUNT and col>=0 and is_valid_location(board,col):
                    numero = True
                    row = get_next_open_row(board, col)
                    drop_piece(board,row,col,1)            
                else:
                    1/0
            except:
                print('Movimento inválido. Tente novamente.')
        turn=1
    else:
        numero = False
        while not numero:
            col = input("Jogador 2 faz a jogada (0-6): ")
            try:
                col = int(col)
                if col<COLUMN_COUNT and col>=0 and is_valid_location(board,col):
                    numero = True
                    row = get_next_open_row(board, col)
                    drop_piece(board,row,col,2)
                else:
                    1/0
            except:
                print('Movimento inválido. Tente novamente.')
        turn = 0
    game_over = winning_move(board,row,col)
    print_board(board)

print("GAME OVER")
print("VITÓRIA DO JOGADOR", int(board[row][col]))