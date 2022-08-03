from time import sleep
import pygame
from pygame import *
import numpy as np

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BOARD_COLOR = (255, 204, 102)


done = True
wrong = False
invalid = None

pad = 40
cell_size = 50
dol_size = 40
board_width, board_height = 15, 15
w = cell_size * (board_width - 1) + pad * 2 # 한칸 크기*칸의 개수 + 좌우 여백 => 가로 크기
h = cell_size * (board_height - 1) + pad * 2 # 한칸 크기*칸의 개수 + 상하 여백 => 세로 크기
_h = cell_size * (board_height - 1) + pad * 2 + (cell_size*3)

global dol_order

dol_order = np.zeros(board_width*board_height).astype('int').reshape(15,15)

global px, py

win_black = None # 검은색이 이긴 경우 True, 그것이 아니면 False
win_white = None # 흰색이 이긴 경우 True, 그것이 아니면 False

black_count = 0
white_count = 0

turn = 0 # 순서 변수

img_black_dol = pygame.image.load("./go_black.png")
img_black_dol = pygame.transform.scale(img_black_dol, (dol_size,dol_size))
img_white_dol = pygame.image.load("./go_white.png")
img_white_dol = pygame.transform.scale(img_white_dol, (dol_size,dol_size))
img_purin = pygame.image.load("./purin.jpeg")
img_purin = pygame.transform.scale(img_purin, (dol_size*2, dol_size*2))
img_check = pygame.image.load("./check.png")
img_check = pygame.transform.scale(img_check, (dol_size, dol_size))

pygame.font.init()
ft = pygame.font.SysFont('Apple Gothic', 40, True, False)


def DrawBoard():
    for i in range(board_height):
            pad_y = pad + (i * cell_size)
            pad_x = pad + (i * cell_size)

            pygame.draw.line(screen, BLACK, (pad, pad_y), (w-pad, pad_y), 3)
            pygame.draw.line(screen, BLACK, (pad_x, pad), (pad_x, h-pad), 3)
	    
    pygame.display.flip()

def DrawDol(x, y):
    screen.blit(img_black_dol, (x, y))

    pygame.display.flip()

def DrawMenu():
    screen.blit(img_black_dol, (30, 850))
    screen.blit(img_white_dol, (300, 850))
    screen.blit(img_purin, (550, 830))

    pygame.display.flip()

pygame.init()

global screen
screen = pygame.display.set_mode((w, _h)) 

clock = pygame.time.Clock() 

screen.fill(BOARD_COLOR)

DrawBoard()
#DrawMenu()

while done:

    clock.tick(10)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

        if event.type == pygame.MOUSEBUTTONUP:
            if wrong == True:
                wrong = False
            
            else:
                turn += 1

            print(turn)
            #pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN:
            column_index, row_index = pygame.mouse.get_pos()

            nomal_column_index = column_index - pad
            nomal_row_index = row_index - pad

            _px = nomal_column_index % cell_size
            _py = nomal_row_index % cell_size

            if _px < 25 :
                px = (nomal_column_index // cell_size) * cell_size
            else:
                px = ((nomal_column_index // cell_size) + 1) * cell_size
            
            if _py < 25 :
                py = (nomal_row_index // cell_size) * cell_size
            else:
                py = ((nomal_row_index // cell_size) + 1) * cell_size


            # 검은돌 차례일 떄
            if turn%2 == 0:
                #px//50, py//50 -> 배열 인덱스
                dim_px = px//50
                dim_py = py//50

                screen.blit(img_check, (400, 850))

                if dim_px < 0 or dim_px > board_width or dim_py < 0 or dim_py > board_height:
                    print("범위 밖에 위치임", end = '\n')
                    text = ft.render("범위 밖에 위치임", True, RED)
                    screen.blit(text, (200, 770))
                    invalid = True

                else :
                    # 이미 그 자리에 돌이 있는 경우에는 에러 메시지 출력
                    if dol_order[dim_px][dim_py] == 1 or dol_order[dim_px][dim_py] == 2:
                        wrong = True
                        print("이미 돌이 있음", end = '\n')

                    # 그것이 아니라면 그림 그리기
                    else :
                        screen.blit(img_black_dol, (px + (dol_size//2), py + (dol_size//2)))
                        dol_order[dim_px][dim_py] = 1 # 검은 돌임을 의미

                        #우, 하, 우대, 좌대
                        dr = [0, 1, 1, 1]
                        dc = [1, 0, 1, -1]

                        for start_r in range(board_height):
                            for start_c in range(board_width):
                                if dol_order[start_r][start_c] == 1:
                                    for d in range(4):
                                        r = start_r
                                        c = start_c
                                        cnt = 0

                                        while 0<= r <= board_height-1 and 0<= c <= board_width - 1 and dol_order[r][c] == 1:
                                            cnt += 1
                                            r += dr[d]
                                            c += dc[d]
                                        
                                        if cnt >= 5:
                                            win_black = True
                                            win_white = False
                    
                        # checkWinner()
                        

                        if win_black == True:
                            print("검은 돌 승리!")
                            text = ft.render("검은 돌 승리!", True, BLUE)
                            screen.blit(text, (200, 770))
                            done = False
                        
                
            # 흰돌 차례일때    
            else:
                
                dim_px = px // 50
                dim_py = py // 50

                if dim_px < 0 or dim_px > board_width or dim_py < 0 or dim_py > board_height:
                    print("범위 밖의 위치임", end = '\n')
                    text = ft.render("범위 밖에 위치임", True, RED)
                    screen.blit(text, (200, 770))
                    wrong = True
                    invalid = True

                else :

                    # 이미 그 자리에 돌이 있는 경우에는 에러 메시지 출력
                    if dol_order[dim_px][dim_py] == 1 or dol_order[dim_px][dim_py] == 2:
                        wrong = True
                        print("이미 돌이 있음", end = '\n')

                    # 그것이 아니라면 그림 그리기
                    else :
                        screen.blit(img_white_dol, (px + (dol_size//2), py + (dol_size//2)))
                        dol_order[dim_px][dim_py] = 2

                        #우, 하, 우대, 좌대
                        dr = [0, 1, 1, 1]
                        dc = [1, 0, 1, -1]

                        for start_r in range(board_height):
                            for start_c in range(board_width):
                                if dol_order[start_r][start_c] == 2:
                                    for d in range(4):
                                        r = start_r
                                        c = start_c
                                        cnt = 0

                                        while 0<= r <= board_height-1 and 0<= c <= board_width - 1 and dol_order[r][c] == 2:
                                            cnt += 1
                                            r += dr[d]
                                            c += dc[d]
                                        
                                        if cnt >= 5:
                                            win_white = True
                                            win_black = False


                    

                        # checkWinner()

                        if win_white == True:
                            print("흰 돌 승리!")
                            text = ft.render("흰 돌 승리!", True, BLUE)
                            screen.blit(text, (200, 770))
                            done = False
                        
                
            print("Column Index and Row Index", end = '\n')
            print(column_index, row_index)

            print("Px and Py", end = '\n')
            print(px, py)
            print("\n")


    pygame.display.flip()
    
    
    
sleep(3) # 게임 종료후 3초 뒤에 자동으로 종료하도록 하기 위함
pygame.quit()
