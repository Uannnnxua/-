import os
import math
import time
import json
import pygame 
import random
import numpy as np
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
        pygame.display.set_caption('picture')
        self.white = (235, 215, 155)
        self.running = True 
        self.x = self.WIDTH // 2
        self.y = self.HEIGHT // 2
        self.speed = 5
        self.goback = self.goback() # 連接、定義回朔、訂定初始化 goback

        # 遊戲總時間
        self.game_all_time = 60

        # 遊戲加、減分 and 加降速設置
        self.got_point = 0
        self.star_list = []
        self.unpoint_list = []
        self.high_score = self.gameover_point() # 讀取最高分數
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

    # ----------------------儲存與輸出最高分數------------------------
    def gameover_point(self):
        # json 儲存檔案
        if os.path.exists("data.json"):
            with open('data.json', 'r') as f:
                try:
                    data = json.load(f)
                    return data.get('high_score', 0) # 讀取資料
                except json.JSONDecodeError:
                    return 0
        return 0
    
    def remove_score(self):
        if self.got_point > self.high_score:
            self.high_score = self.got_point
            with open('data.json', 'w+') as f:
                json.dump({'high_score': self.high_score}, f)
    # ----------------------------------------------------------------

    def run_game(self):
        # 回朔時間設定
        self.downloadtime = time.time()
        # 遊戲計時設定
        self.run_game_time = time.time()

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) # 設定視窗大小
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
            
            show_high_score = font.render(f'High score: ' + str(int(self.high_score)), True, (48,25,52)) # 後三項為數字
            self.screen.blit(show_high_score, (720, 10))
            print(1)

            pygame.display.update()
            
            if remaining_time <= 0:
                self.running = False
        self.remove_score()
        pygame.quit()

    def show_menu(self):
        pygame.init()
        menu_running = True 
        font = pygame.font.Font(None, 50)  # 設定字體和大小
        WITH, HEGHT = 500, 500
        screen = pygame.display.set_mode((WITH, HEGHT))

        # 按鈕屬性設定
        open_button = pygame.Rect(WITH // 2 - 90, 200, 195, 35) #　四邊ｘ，ｙ座標
        close_button = pygame.Rect(WITH // 2 - 90, 300, 195, 35)
        button_color = (255, 255, 255)

        while menu_running:
            screen.fill((200, 200, 200))  # 設定選單背景顏色

            # 繪製按鈕
            pygame.draw.rect(screen, button_color, open_button)
            pygame.draw.rect(screen, button_color, close_button)

            # 顯示選項文字
            title_text = font.render("Game Menu", True, (0, 0, 0))
            start_text = font.render("Start Game", True, (0, 0, 0))
            quit_text = font.render("Quit", True, (0, 0, 0))

            # 將文字繪製到按鈕上
            screen.blit(title_text, (WITH // 2 - 100, 100))
            screen.blit(start_text, (WITH // 2 - 85, 200))
            screen.blit(quit_text, (WITH // 2 - 35, 300))

            pygame.display.update() # 重製視窗

            # 監聽選單事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    pygame.quit()
                    return
                    # 結束遊戲
                elif event.type == pygame.MOUSEBUTTONDOWN: # 監聽滑鼠當滑鼠按鍵遭點擊
                    # 遭點擊後反應
                    if open_button.collidepoint(event.pos):  # event.pos 為收到點擊後
                        menu_running = False
                        self.running = True # 進入遊戲
                        # 資料初始化
                        game.run_game()
                    elif close_button.collidepoint(event.pos):  
                        menu_running = False
                        pygame.quit() # 如按下退出鍵結束視窗s
                        return init

        



player_coler = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # 隨機角色顏色
init = True
if __name__ == '__main__':
    game = pyg() # 連接class   
    while True:
        game.show_menu()