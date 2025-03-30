import math
import time
import pygame 
import numpy as np
import random
import tkinter as Tk
from tkinter import *

class pyg:
    class goback(): # 回復至上一步
        
        def __init__(self):
            self.history = [] # 使用陣列紀錄資料
            self.firststatus = np.array([0,0]) # 訂定初始化 
        
        def add_lastmove(self, firststatus): # 新增至陣列尾端
            self.history.append(firststatus.copy()) # append 新增至陣列尾端 copy 複製初始資料

        def back_lastmove(self):
            if self.history:
                return self.history.pop() # 用 POP 刪除最一次回朔紀錄

    def __init__(self):
        self.WIDTH = 900
        self.HEIGHT = 600        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) # 設定視窗大小
        pygame.display.set_caption('picture')
        self.white = (235, 215, 155)
        self.running = True 
        self.x = self.WIDTH // 2
        self.y = self.HEIGHT // 2
        self.speed = 5
        self.downloadtime = time.time()
        self.goback = self.goback() # 連接、定義回朔、訂定初始化 goback
        # 遊戲計時設定
        self.run_game_time = time.time()
        self.game_all_time = 60

        # 遊戲加、減分 and 加降速設置
        self.got_point = 0
        self.star_list = []
        self.unpoint_list = []
        self.last_time_star = time.time() # 上一次星星所生成時間
        self.last_time_unpoint = time.time()

    def move(self, direction): # direction 收到監聽鍵盤後做出指定反應的中介函數
        self_dewnload = time.time()
        if self_dewnload - self.downloadtime > 5: # 五秒記錄一次位置
            self.downloadtime = self_dewnload       
            self.goback.add_lastmove(np.array([self.x, self.y]))
        if self.y > 0 and self.y < 595 and self.x > 0 and self.x < 895:
            if direction == 'UP':
                self.y -= self.speed
            elif direction == 'DOWN':
                self.y += self.speed
            elif direction == 'LEFT':
                self.x -= self.speed
            elif direction == 'RIGHT':
                self.x += self.speed
        elif self.y <= 100:
            self.y += self.speed
        elif self.y >= 595:
            self.y -= self.speed
        elif self.x <= 5:
            self.x += self.speed
        elif self.x >= 895:
            self.x -= self.speed

    def real_back(self):
        sem = self.goback.back_lastmove() # 回朔上一步 
        if isinstance(sem, np.ndarray) and sem.size == 2:    
            self.x, self.y = sem # sem stasus end move
        
    def point(self, surface, center, size):
        x, y = center
        points = []
        for i in range(5): # 星型的五邊
            angel = i * 2 * math.pi / 5 - math.pi / 2 # 角度依照三角形公式計算
            # 用三角函式計算出頂點座標
            outer_x = x + size * math.cos(angel)
            outer_y = y + size * math.sin(angel)
            points.append((outer_x, outer_y))
            angel += math.pi / 5
            inner_x = x + size / 2 * math.cos(angel)
            inner_y = y + size / 2 * math.sin(angel)
            points.append((inner_x, inner_y))
            i += 1
        self.point_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.polygon(surface, self.point_color, points)


        
    def print_star(self):
        now_time = time.time() # time 函式輸入當下時間
        if now_time - self.last_time_star > 1: # 2.5秒生成一顆星星
            star_x = random.randint(10,890)
            star_y = random.randint(10,590)
            self.star_list.append([star_x, star_y])
            self.last_time_star = now_time # 更新最後生成時間    

    def will_touchstar(self):
        for star in self.star_list:
            distance = math.sqrt((self.x - star[0]) ** 2 + (self.y - star[1]) ** 2) # 計算角色與星星的距離
            if distance < 10: # 判斷角色與星星的距離
                self.star_list.remove(star)
                self.speed += 1 
                self.got_point += 1

    def unpoint(self):
        unpoint_now_time = time.time()
        if unpoint_now_time - self.last_time_unpoint > 3:
            unpoint_x = random.randint(10,890)
            unpoint_y = random.randint(10,590)
            self.unpoint_list.append([unpoint_x, unpoint_y])
            self.last_time_unpoint = unpoint_now_time # 計算時間生成扣分方塊

    def will_touchunpoint(self):
        for unpoint in self.unpoint_list:
            distance = math.sqrt((self.x - unpoint[0]) ** 2 + (self.y - unpoint[1]) ** 2)
            if distance < 10:
                self.unpoint_list.remove(unpoint)
                self.speed -= 1
                self.got_point -= 1

    def run_game(self):
        pygame.init()
        while self.running:
            pygame.time.delay(20) # 執行迴圈延遲

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False # 退出

            keys = pygame.key.get_pressed() # 監聽上下左右鍵並且設定操作指令
            if keys[pygame.K_UP]:
                self.move('UP')
            elif keys[pygame.K_LEFT]:
                self.move('LEFT')
            elif keys[pygame.K_RIGHT]:
                self.move('RIGHT')
            elif keys[pygame.K_DOWN]:
                self.move('DOWN')
            elif keys[pygame.K_F7]:
                self.real_back()

            self.print_star() # 生成出星星
            self.unpoint() # 生成減分方塊
            self.will_touchstar()
            self.will_touchunpoint()

            self.screen.fill(self.white) # background

            for star in self.star_list:
                self.point(self.screen, star, 5)
            for unpoint in self.unpoint_list:
                pygame.draw.rect(self.screen, (255, 0, 0), (unpoint[0], unpoint[1], 10, 10))
            pygame.draw.circle(self.screen, player_coler, (self.x, self.y), 20)

            # 時間顯示 and 退出判定
            font = pygame.font.Font(None, 36) # 設定字體大小
            player_last_time = time.time() - self.run_game_time
            remaining_time = max(0, self.game_all_time - player_last_time) # 最小值不能小於零以防負數計時
            # render 初始化字體調整對象並調整輸出文字為圖像
            show_time = font.render(f'Time: ' + str(int(remaining_time)), True, (125, 125, 125))
            # 顯示圖片輸出位置
            self.screen.blit(show_time, (10, 10))

            show_got_point = font.render(f'Got point: ' + str(int(self.got_point)), True, (200,200,200))
            self.screen.blit(show_got_point, (390, 10))


            pygame.display.update()
            
            if remaining_time <= 0:
                self.running = False
       
        pygame.quit()
    

player_coler = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # 隨機角色顏色

if __name__ == '__main__':
    game = pyg() # 連接class
    while True:        
        game.run_game()