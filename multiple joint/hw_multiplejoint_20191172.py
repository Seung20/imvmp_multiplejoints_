# Draw a robot arm with multiple joints, controlled with keyboard inputs
#
# -*- coding: utf-8 -*- 

import pygame
import numpy as np
from pygame.locals import *
import os

# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)



def Rmat(deg):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R

def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H


# Pygame 초기화
pygame.init()

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')


sound_1 = pygame.mixer.Sound(os.path.join(assets_path, 'fizzle.mp3'))
sound_2= pygame.mixer.Sound(os.path.join(assets_path, 'fizzle_2.mp3'))

# 윈도우 제목
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False
# 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
font = pygame.font.SysFont('FixedSys', 40, True, False)

# poly: 4 x 3 matrix
poly = np.array( [[0, 0, 1], [100, 0, 1], [100, 20, 1], [0, 20, 1]])
poly_2 = np.array([[0, 0, 1], [20, 0, 1], [20, 50, 1], [0, 50, 1]])
poly_3 = np.array([[0, 0, 1], [40, 0, 1], [40, 10, 1], [0, 10, 1]])



poly = poly.T # 3x4 matrix 
poly_2 = poly_2.T
poly_3 = poly_3.T

cor_1 = np.array([10, 10, 1])
cor_2 = np.array([10,5,1])

degree = 300

#x는 로봇의 degree를 움직이기 위한 변수
x = 0
#x_a는 로봇의 전체 x 좌표를 움직이기 위한 변수
x_a = 0
y_b= 600

#x_f 는 로봇의 x좌표
x_f = 300


# 게임 반복 구간
while not done:
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #방향키 상하는 각각 각도 조절, 좌우는 로봇 전체의 x좌표 움직임
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                x+=1
            elif event.key == pygame.K_DOWN:
                x-=1
            elif event.key == pygame.K_LEFT:
                x_a -= 5
            elif event.key == pygame.K_RIGHT:
                x_a += 5
            #키보드에 손을 뗄 때 효과음이 들리도록 설정했다.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                x=0 
                sound_1.play()
            elif event.key == pygame.K_DOWN:
                x=0
                sound_2.play()

            elif event.key == pygame.K_LEFT:
                x_a=0
            elif event.key == pygame.K_RIGHT:
                x_a= 0

# 윈도우 화면 채우기
    screen.fill(WHITE)

    # 다각형 그리기
    # poly: 3xN 9
    
    #로봇의 x좌표 움직이기
    x_f += x_a
    #로봇 arm의 최초 몸통
    pygame.draw.polygon(screen, BLACK, [[(x_f)-10,600],[(x_f)-10, 699], [(x_f)+30,699], [(x_f)+30, 600]], 4)
    
    #바퀴
    pygame.draw.circle(screen, GREY, [(x_f)-10, 690], 10)
    pygame.draw.circle(screen, GREY, [(x_f)+30, 690], 10)
    

    #로봇의 각도에 따라서 꺾이지 않게끔 기준을 설정
    if 300 <= degree <= 360:
        degree += x
    elif degree > 360:
        degree -= 1
    else:
        degree += 1


    H = Tmat(x_f, y_b) @ Tmat(10, 10) @ Rmat(degree) @ Tmat(-10, -10)
    K = H @ Tmat(80,0) @ Tmat(10, 10) @Rmat(degree) @ Tmat(-10, -10)
    T = K @ Tmat(80,0) @ Tmat(10, 10) @Rmat(degree) @ Tmat(-10, -10)
    I = T @ Tmat(80,0) @ Tmat(10, 10) @Rmat(degree) @ Tmat(-10, -10)
    J = I @ Tmat(80,0) @ Tmat(10, 10) @Rmat(degree) @ Tmat(-10, -10)

    #로봇 arm의 끝, 손 부분
    L = J @ Tmat(80,-15)
    A = J @ Tmat(80, 35)
    AA = J @ Tmat(80, -25)
    
    
    # print(Tmat(300,600))
    
    #로봇 arm의 마디
    corp = H @ cor_1
    corp_2 = K @ cor_1
    corp_3 = T @ cor_1
    corp_4 = I @ cor_1
    corp_5 = J @ cor_1

    #arm의 끝부분 손의 마디
    corp_7 = A @ cor_2
    corp_8 = AA @ cor_2

    


    pp = H @ poly
    pp_2 = K @ poly
    pp_3 = T @ poly
    pp_4 = I @ poly
    pp_5 = J @ poly

    HH_1 = L @ poly_2
    HR = A @ poly_3
    HH_3 = AA @ poly_3

    q = pp[0:2, :].T # N x 2 matrix
    r = pp_2[0:2, :].T
    s = pp_3[0:2, :].T
    t = pp_4[0:2, :].T
    u = pp_5[0:2, :].T
    v = HH_1[0:2, :].T
    w = HR[0:2, :].T
    y = HH_3[0:2, :].T
   

    # print(pp.shape, pp, pp.T )
    # pygame.draw.polygon(screen, RED, [300,650], 4)
   
    
    

    pygame.draw.polygon(screen, BLACK, q, 4)
    pygame.draw.polygon(screen, BLACK, r, 4)
    pygame.draw.polygon(screen, BLACK, s, 4)
    pygame.draw.polygon(screen, BLACK, t, 4)
    pygame.draw.polygon(screen, BLACK, u, 4)
    pygame.draw.polygon(screen, BLACK, v, 4)
    pygame.draw.polygon(screen, BLACK, w, 4)
    pygame.draw.polygon(screen, BLACK, y, 4)



    pygame.draw.circle(screen, (0, 0, 0), corp[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_2[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_3[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_4[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_5[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_7[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_8[:2], 3)

    # print(corp[:2])

    # 안티얼리어스를 적용하고 검은색 문자열 렌더링
    text = font.render("Robot arm", True, BLACK)
    screen.blit(text, [WINDOW_WIDTH/2-70, 0])

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)  

# 게임 종료
pygame.quit()