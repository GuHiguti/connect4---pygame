from pygame.locals import *
from sys import exit
import numpy as np
import pygame
import colors

ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_POINTS_COUNT = 4
PLAYER1_COLOR = colors.orange()
PLAYER2_COLOR = colors.red()

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

def draw_reference(pos, turn):
    pygame.draw.rect(scr,colors.black(),(0,0,width,SQUARE_SIZE))
    if turn==0:
        pygame.draw.circle(scr,PLAYER1_COLOR,pos,(SQUARE_SIZE/2)-5)
    elif turn==1:
        pygame.draw.circle(scr,PLAYER2_COLOR,pos,(SQUARE_SIZE/2)-5)

def draw_board(board):
    board = list(reversed(board))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(scr, colors.blue(), (c*SQUARE_SIZE,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            cor = colors.black()
            if int(board[r][c])==1:
                cor = PLAYER1_COLOR
            elif int(board[r][c])==2:
                cor = PLAYER2_COLOR
            pygame.draw.circle(scr,cor,(c*SQUARE_SIZE+SQUARE_SIZE/2,r*SQUARE_SIZE+SQUARE_SIZE/2+SQUARE_SIZE),(SQUARE_SIZE/2)-5)

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
    if seq_diag_left>=WIN_POINTS_COUNT:
        return True
    return False

board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100
width = COLUMN_COUNT  * SQUARE_SIZE
height= (ROW_COUNT+1) * SQUARE_SIZE
size = (width, height)
myfont = pygame.font.SysFont("monospace", 75)

scr = pygame.display.set_mode(size)
draw_board(board)

while not game_over:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEMOTION:
            draw_reference((max(min(event.pos[0],width-SQUARE_SIZE/2),SQUARE_SIZE/2),SQUARE_SIZE/2),turn)

        if event.type == MOUSEBUTTONDOWN:
            if turn==0:
                numero = False
                while not numero:
                    col = int(event.pos[0]/SQUARE_SIZE)
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
                    #col = input("Jogador 2 faz a jogada (0-6): ")
                    col = int(event.pos[0]/SQUARE_SIZE)
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
            print_board(board)
            draw_board(board)   
            game_over = winning_move(board,row,col)
            if game_over:
                cor = colors.black()
                if turn==0:
                    turn=2
                    cor = PLAYER2_COLOR
                else: 
                    turn = 1
                    cor = PLAYER1_COLOR
                pygame.draw.rect(scr,colors.black(),(0,0,width,SQUARE_SIZE))
                label = myfont.render("PLAYER "+str(turn)+" WIN!!!",0,cor)
                pygame.Surface.blit(scr,label,(0,0,width,height))
                pygame.display.update()
                pygame.time.wait(2000)
                break
            draw_reference((max(min(event.pos[0],width-SQUARE_SIZE/2),SQUARE_SIZE/2),SQUARE_SIZE/2),turn)

print("GAME OVER")
print("VITÓRIA DO JOGADOR", int(board[row][col]))